import os
from typing import Dict

from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.readers.entity.formats.csv_entity_format import CsvEntityFormat
from gen_common.data.readers.entity.formats.folder_entity_format import FolderEntityFormat
from gen_common.data.readers.entity.formats.json_entity_format import JsonEntityFormat
from gen_common.data.readers.entity.formats.xml_entity_format import XmlEntityFormat
from gen_common.util.json_util import JsonUtil


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
    def get_parser(cls, data_path: str, definition: Dict = None) -> AbstractEntityFormat:
        """
        :param data_path: Path to folder containing project data.
        :param definition: The project definition.
        :return: Returns the function that will read data into a data frame.
        """
        if definition and StructuredKeys.PARSER in definition:
            parser_key = JsonUtil.get_property(definition, StructuredKeys.PARSER).upper()
            return SupportedEntityFormats.FORMATS[parser_key]
        if os.path.isdir(data_path):
            return SupportedEntityFormats.FORMATS["FOLDER"]
        for _, entity_format in cls.FORMATS.items():
            if entity_format.is_format(data_path):
                return entity_format

        supported_file_types = [f.lower() for f in cls.FORMATS.keys()]
        raise ValueError(data_path, "does not have supported file type: ", supported_file_types)
