import os
from typing import List

import pandas as pd

from data.datasets.creators.readers.entity.entity_reader import EntityReader, EntityType
from data.datasets.keys.structure_keys import StructureKeys


class PreTrainReader(EntityReader[List[str]]):
    DELIMINATOR = "\n"

    def __init__(self, data_path: str):
        base_path, file_name = os.path.split(data_path)
        super().__init__(base_path, {
            StructureKeys.PATH: file_name,
            StructureKeys.PARSER: "FOLDER"
        })

    def create(self, entity_df: pd.DataFrame) -> EntityType:
        examples = []
        for entity_index, entity_row in entity_df.iterrows():
            file_content = entity_row[StructureKeys.Artifact.BODY]
            for example in file_content.split(self.DELIMINATOR):
                examples.append(example)
        return examples
