import os
from typing import Dict

from data.datasets.creators.readers.entity.entity_parser_type import EntityParserType
from data.datasets.creators.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from data.datasets.creators.readers.entity.formats.csv_entity_format import CsvEntityFormat
from data.datasets.creators.readers.entity.formats.folder_entity_format import FolderEntityFormat
from data.datasets.creators.readers.entity.formats.json_entity_format import JsonEntityFormat
from data.datasets.creators.readers.entity.formats.xml_entity_format import XmlEntityFormat
from data.datasets.keys.structure_keys import StructureKeys
from util.json_util import JsonUtil


class SupportedEntityFormats:
    """
    The available method for reading a set of entities from a file
    or folder.
    """

    FORMATS: Dict[str, AbstractEntityFormat] = {
        "XML": XmlEntityFormat,
        "CSV": CsvEntityFormat,
        "FOLDER": FolderEntityFormat,
        "JSON": JsonEntityFormat
    }

    @classmethod
    def get_parser(cls, data_path: str, definition: Dict = None) -> EntityParserType:
        """
        :return: Returns the function that will read data into a data frame.
        """
        if definition and StructureKeys.PARSER in definition:
            parser_key = JsonUtil.get_property(definition, StructureKeys.PARSER).upper()
            return SupportedEntityFormats.FORMATS[parser_key].get_parser()
        if os.path.isdir(data_path):
            return SupportedEntityFormats.FORMATS["FOLDER"].get_parser()
        for _, entity_format in cls.FORMATS.items():
            if entity_format.is_format(data_path):
                return entity_format.get_parser()

        supported_file_types = [f.lower() for f in cls.FORMATS.keys()]
        raise ValueError(data_path, "does not have supported file type: ", supported_file_types)
