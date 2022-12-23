import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Dict, Generic, Optional, Type, TypeVar

import pandas as pd

from data.formats.safa_format import SafaFormat
from data.readers.project.structure_keys import StructureKeys
from util.dataframe_util import DataFrameUtil
from util.file_util import FileUtil
from util.json_util import JSONUtil


class Wrapper:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        print(self.f)
        return self.f(*args, **kwargs)


def read_folder(folder_path: str, exclude=None):
    """
    Creates artifact for each file in folder path.
    :param folder_path: Path to folder containing artifact files.
    :param exclude: The files to exclude in folder path.
    :return: DataFrame containing artifact ids and tokens.
    """
    if exclude is None:
        exclude = [".DS_Store"]
    items = list(filter(lambda f: f not in exclude, os.listdir(folder_path)))
    entries = []
    for item in items:
        file_path = os.path.join(folder_path, item)
        entry = {
            SafaFormat.ARTIFACT_ID: item,
            SafaFormat.SAFA_CVS_ARTIFACT_TOKEN: FileUtil.read_file(file_path)
        }
        entries.append(entry)
    return pd.DataFrame(entries)


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


class EntityReader(ABC, Generic[EntityType]):
    """
    Responsible for converting data into entities.
    """

    def __init__(self, base_path: str, definition: Dict, conversions: Dict = None):
        """
        Creates reader
        :param base_path: The base path to find data.
        :param definition: Defines how to parse the data.
        :param conversions: The conversions to the data to standardize it.
        """
        required_properties = [StructureKeys.PATH]
        JSONUtil.require_properties(definition, required_properties)

        self.definition: Dict = definition
        self.path = os.path.join(base_path, self.get_property(StructureKeys.PATH))
        self.conversions: Dict[str, Dict] = conversions if conversions else None
        self.entity_type = None

    def get_entities(self):
        if self.entity_type is None:
            entity_df = self.read_entities()
            self.entity_type = self.create(entity_df)
        return self.entity_type

    @abstractmethod
    def create(self, entity_df) -> EntityType:
        pass

    def read_entities(self) -> pd.DataFrame:
        source_entities_df = self.read_source_entities()
        column_conversion = self.read_column_conversion()
        return DataFrameUtil.convert_columns(source_entities_df, column_conversion)

    def read_source_entities(self):
        parser_params = self.get_property(StructureKeys.PARAMS) if StructureKeys.PARAMS in self.definition else {}
        parser = EntityReader.get_entity_parser(self.path)
        return parser(self.path, **parser_params)

    def read_column_conversion(self) -> Optional[Dict]:
        if StructureKeys.COLS in self.definition:
            conversion_id = self.get_property(StructureKeys.COLS)
            assert self.conversions is not None, "Could not find conversion %s because none defined." % conversion_id
            return self.conversions[conversion_id]
        return None

    def get_property(self, property_name: str, default_value=None):
        if property_name not in self.definition and not default_value:
            raise ValueError(self.definition, "does not contain property: ", property_name)
        return self.definition.get(property_name, default_value)

    @staticmethod
    def get_entity_parser(entity_path) -> Type[Callable]:
        if os.path.isdir(entity_path):
            return EntityFormats.FOLDER.value
        data_file_name = os.path.basename(entity_path)
        for f, extensions in EntityFileTypes:
            for extension in extensions:
                if extension in data_file_name:
                    return f.value

        supported_file_types = [f.name.lower() for f in EntityFormats]
        raise Exception(data_file_name, "does not have supported file type: ", supported_file_types)
