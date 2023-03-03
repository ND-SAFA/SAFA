import os
from typing import List

from data.readers.entity.entity_reader import EntityReader
from data.keys.structure_keys import StructuredKeys
from util.base_object import BaseObject


class PreTrainProjectReader(BaseObject):
    """
    Responsible for reading pre-training examples from series of files.
    """
    DELIMINATOR = "\n"

    def __init__(self, data_path: str):
        """
        Constructs pre-training reader targeted at path to folder.
        :param data_path: Path to folder containing pre-training files.
        """
        base_path, file_name = os.path.split(data_path)
        self.entity_reader = EntityReader(base_path, {
            StructuredKeys.PATH: file_name,
            StructuredKeys.PARSER: "FOLDER"
        })

    def create(self) -> List[str]:
        """
        Reads files in folder and aggregates examples in each file.
        :return: List lines found across files in folder.
        """
        entity_df = self.entity_reader.read_entities()
        examples = []
        for _, entity_row in entity_df.iterrows():
            file_content = entity_row[StructuredKeys.Artifact.CONTENT.value]
            for example in file_content.split(self.DELIMINATOR):
                examples.append(example)
        return examples
