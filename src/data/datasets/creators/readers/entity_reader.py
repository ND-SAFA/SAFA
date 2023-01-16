import os
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

import pandas as pd

from data.datasets.keys.structure_keys import StructureKeys
from util.dataframe_util import DataFrameUtil
from util.file_util import FileUtil
from util.json_util import JSONUtil
from util.reflection_util import ReflectionUtil


class Wrapper:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


def read_files_as_artifacts(file_paths: List[str], use_file_name: bool = True):
    """
    Reads file at each path and creates artifact with name
    :param file_paths: List of paths to file to read as artifacts
    :param use_file_name: Whether to use file name as artifact id, otherwise file path is used.
    :return: DataFrame containing artifact properties id and body.
    """
    entries = []
    for file_path in file_paths:
        artifact_name = os.path.basename(file_path) if use_file_name else file_path
        entry = {
            StructureKeys.Artifact.ID: artifact_name,
            StructureKeys.Artifact.BODY: FileUtil.read_file(file_path)
        }
        entries.append(entry)
    return pd.DataFrame(entries)


def read_folder(path: str, exclude=None):
    """
    Creates artifact for each file in folder path.
    :param path: Path to folder containing artifact files.
    :param exclude: The files to exclude in folder path.
    :return: DataFrame containing artifact ids and tokens.
    """
    files_in_path = FileUtil.get_file_list(path, exclude=exclude)
    return read_files_as_artifacts(files_in_path)


def read_json(data_path: str, entity_name: str = None):
    data = FileUtil.read_json_file(data_path)
    if entity_name is None:
        keys = list(data.keys())
        assert len(keys) == 1, "Found multiple keys for entities."
        entity_name = keys[0]
    return pd.DataFrame(data[entity_name])


class EntityFormats(Enum):
    """
    The available method for reading a set of entities from a file
    or folder.
    """
    XML = Wrapper(pd.read_xml)
    CSV = Wrapper(pd.read_csv)
    FOLDER = Wrapper(read_folder)
    JSON = Wrapper(read_json)


EntityFileTypes = [
    (EntityFormats.XML, [".xml"]),
    (EntityFormats.CSV, [".csv", ".txt"]),
    (EntityFormats.JSON, [".json"])
]

EntityType = TypeVar("EntityType")


class EntityReader(Generic[EntityType]):
    """
    Responsible for converting data into entities.
    """

    def __init__(self, base_path: str, definition: Dict, conversions: Dict = None, overrides: Dict = None):
        """
        Creates entity reader for project at base_path using definition given.
        :param base_path: The base path to find data.
        :param definition: Defines how to parse the data.
        :param conversions: The definitions to the data to standardize it.
        :param overrides: The properties to override in class if they exist.
        """
        required_properties = [StructureKeys.PATH]
        JSONUtil.require_properties(definition, required_properties)
        self.definition: Dict = definition
        self.path = os.path.join(base_path, self._get_property(StructureKeys.PATH))
        self.conversions: Dict[str, Dict] = conversions if conversions else None
        self.entity_type = None
        self._set_properties(self, overrides)

    def read_entities(self) -> pd.DataFrame:
        """
        Reads original entities and applies any column conversion defined in definition.
        :return: DataFrame containing processed entities.
        """
        source_entities_df = self._read_original_entities()
        column_conversion = self._read_column_conversion()
        processed_df = DataFrameUtil.rename_columns(source_entities_df, column_conversion)
        return processed_df

    def _read_original_entities(self) -> pd.DataFrame:
        """
        Reads data and aggregates examples into data frame.
        :return: DataFrame containing original examples
        """
        parser_params = self._get_property(StructureKeys.PARAMS, {})
        parser = self._get_entity_parser()
        return parser(self.path, **parser_params)

    def _read_column_conversion(self) -> Optional[Dict]:
        """
        Reads the column conversion to apply to given source entities.
        :return: Dictionary containing mapping from original column names to target ones.
        """
        if StructureKeys.COLS in self.definition:
            conversion_id = self._get_property(StructureKeys.COLS)
            assert self.conversions is not None, "Could not find conversion %s because none defined." % conversion_id
            return self.conversions[conversion_id]
        return None

    def _get_property(self, property_name: str, default_value=None) -> Any:
        """
        Returns property in definition if exists. Otherwise default is returned is available.
        :param property_name: The name of the property to retrieve.
        :param default_value: The default value to return if property is not found.
        :return: The property under given name.
        """
        if property_name not in self.definition and default_value is None:
            raise ValueError(self.definition, "does not contain property: ", property_name)
        return self.definition.get(property_name, default_value)

    def _get_entity_parser(self) -> Type[Callable]:
        """
        :return: Returns the function that will read data into a data frame.
        """
        if StructureKeys.PARSER in self.definition:
            parser_key = self._get_property(StructureKeys.PARSER).upper()
            return EntityFormats[parser_key].value
        if os.path.isdir(self.path):
            return EntityFormats.FOLDER.value
        data_file_name = os.path.basename(self.path)
        for f, extensions in EntityFileTypes:
            for extension in extensions:
                if extension in data_file_name:
                    return f.value

        supported_file_types = [f.name.lower() for f in EntityFormats]
        raise ValueError(data_file_name, "does not have supported file type: ", supported_file_types)

    @staticmethod
    def _set_properties(obj: Any, properties: Optional[Dict[str, Any]]) -> None:
        """
        Sets key-value in object if they exist.
        :param obj: The object to set properties in.
        :param properties: The properties to override.
        :return: None
        """
        if properties is None:
            return
        properties = {k.upper(): v for k, v in properties.items()}
        ReflectionUtil.set_attributes(obj, properties, missing_ok=True)
