import os
from enum import Enum
from typing import Dict, Type

from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_args import JobArgs
from models.model_manager import ModelManager
from server.serializers.experiment_serializer import ExperimentSerializer
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from train.trainer_args import TrainerArgs
from util.base_object import BaseObject


class DefinitionCreator:
    def __init__(self, definition_class: Type[BaseObject], definition: Dict):
        self.definition_class = definition_class
        self.definition = definition

    def create(self, **kwargs):
        data = self.definition
        data.update(kwargs)
        definition = {ExperimentSerializer.KEY: data}
        experiment_serializer = ExperimentSerializer(data=definition)
        assert experiment_serializer.is_valid(), experiment_serializer.errors
        definition_variable = experiment_serializer.save()
        return self.definition_class.initialize_from_definition(definition_variable)


model_manager_definition_creator = DefinitionCreator(ModelManager, {
    "model_path": "path"
})

job_args_definition_creator = DefinitionCreator(JobArgs, {
    "output_dir": TEST_OUTPUT_DIR
})

trainer_args_definition_creator = DefinitionCreator(TrainerArgs, {
    "output_dir": TEST_OUTPUT_DIR
})

trainer_dataset_manager_definition_creator = DefinitionCreator(TrainerDatasetManager, {
    "train": {
        "objectType": "SAFADatasetCreator",
        "project_path": os.path.join(TEST_DATA_DIR, "safa")
    }
})


class TestData(Enum):
    MODEL_MANAGER: DefinitionCreator = model_manager_definition_creator
    JOB_ARGS: DefinitionCreator = job_args_definition_creator


def get_data(data_type: TestData):
    experiment_serializer = ExperimentSerializer(data=data_type.value)
    assert experiment_serializer.is_valid(), experiment_serializer.errors
    return experiment_serializer.save()
