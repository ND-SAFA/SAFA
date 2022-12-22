import os
from enum import Enum
from typing import Callable, Dict, Type

import pandas as pd

from data.creators.parsers.definitions.structure_keys import StructureKeys
from data.formats.safa_format import SafaFormat
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


EntityFormatFileTypes = [
    (EntityFormats.XML, [".xml"]),
    (EntityFormats.CSV, [".csv", ".txt"]),
    (EntityFormats.JSON, [".json"])
]


class SupportedEntityTypes(Enum):
    ARTIFACT = "artifact"
    TRACE = "trace"


class EntityParser:

    def __init__(self, project_path: str, definition: Dict, conversions=None):
        required_properties = [StructureKeys.FILE]
        JSONUtil.require_properties(definition, required_properties)

        self.definition: Dict = definition
        file_path = os.path.join(project_path, definition[StructureKeys.FILE])
        parser = self.get_entity_parser(file_path)
        parser_params = definition[StructureKeys.PARAMS] if StructureKeys.PARAMS in definition else {}
        self.entity_df = parser(file_path, **parser_params)
        self.conversions = conversions if conversions else None

    def get_entities(self):
        column_conversion = None
        if StructureKeys.COLS in self.definition:
            column_conversion = self.conversions[self.definition[StructureKeys.COLS]]
        return DataFrameUtil.convert_df(self.entity_df, column_conversion)

    @staticmethod
    def get_entity_parser(entity_path) -> Type[Callable]:
        if os.path.isdir(entity_path):
            return EntityFormats.FOLDER.value
        data_file_name = os.path.basename(entity_path)
        for f, extensions in EntityFormatFileTypes:
            for extension in extensions:
                if extension in data_file_name:
                    return f.value

        supported_file_types = [f.name.lower() for f in EntityFormats]
        raise Exception(data_file_name, "does not have supported file type: ", supported_file_types)
