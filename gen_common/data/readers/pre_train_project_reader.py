import os
from typing import List

from gen_common.constants import NEW_LINE
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.entity.entity_reader import EntityReader


class PreTrainProjectReader(AbstractProjectReader[List]):
    """
    Responsible for reading pre-training examples from series of files.
    """

    DELIMINATOR = NEW_LINE

    def __init__(self, project_path: str):
        """
        Constructs pre-training reader targeted at path to folder.
        :param project_path: Path to folder containing pre-training files.
        """
        super().__init__()
        self.base_path, self.file_name = os.path.split(project_path)

    def read_project(self) -> List:
        """
        Reads files in folder and aggregates examples in each file.
        :return: List lines found across files in folder.
        """
        entity_reader = EntityReader(self.base_path, {
            StructuredKeys.PATH: self.file_name,
            StructuredKeys.PARSER: "FOLDER"
        })
        entity_df = entity_reader.read_entities()
        all_examples = []
        for _, entity_row in entity_df.iterrows():
            col_name = StructuredKeys.Artifact.CONTENT.value
            file_content = entity_row[col_name]
            examples = file_content.split(self.DELIMINATOR)
            if self.summarizer is not None:
                examples = self.summarizer.summarize_bulk(bodies=examples)
            all_examples.extend(examples)
        return all_examples

    def get_project_name(self) -> str:
        """
        Get the name of the project
        :return: The name of the project
        """
        return self.file_name
