from copy import deepcopy
from typing import Dict, List

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.creators.split_dataset_creator import SplitDatasetCreator
from data.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from data.datasets.dataset_role import DatasetRole
from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from experiments.variables.typed_definition_variable import TypedDefinitionVariable
from jobs.components.job_args import JobArgs
from models.model_manager import ModelManager
from test.base_test import BaseTest
from test.base_trace_test import BaseTraceTest
from test.definition_creator import DefinitionCreator
from test.paths.paths import TEST_OUTPUT_DIR
from test.test_data_manager import TestDataManager
from train.trainer_args import TrainerArgs


class TestObjectBuilder:
    DATASET_ARGS_PARAMS = {
        "validation_percentage": VALIDATION_PERCENTAGE_DEFAULT
    }

    trainer_args_definition = {
        "output_dir": TEST_OUTPUT_DIR,
        "num_train_epochs": 1,
        "metrics": ["accuracy", "map"]
    }
    job_args_definition = {"output_dir": TEST_OUTPUT_DIR}

    dataset_creator_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "CLASSIC_TRACE",
        "source_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE]),
        "target_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET]),
        "true_links": TestDataManager.get_path(TestDataManager.Keys.TRACES)
    }

    trainer_dataset_manager_definition = {
        "train_dataset_creator": dataset_creator_definition
    }

    model_manager_definition = {
        "model_path": "bert-base-uncased"
    }

    SUPPORTED_OBJECTS = {
        TrainerArgs: trainer_args_definition,
        JobArgs: job_args_definition,
        AbstractDatasetCreator: dataset_creator_definition,
        TrainerDatasetManager: trainer_dataset_manager_definition,
        ModelManager: model_manager_definition
    }

    @staticmethod
    def create_trainer_dataset_manager(dataset_map: Dict[DatasetRole, AbstractDatasetCreator],
                                       split_train_dataset=True) -> TrainerDatasetManager:
        if split_train_dataset:
            dataset_map[DatasetRole.VAL] = SplitDatasetCreator(val_percentage=VALIDATION_PERCENTAGE_DEFAULT)
        return TrainerDatasetManager.create_from_map(dataset_map)

    @staticmethod
    def create_dataset_map(dataset_role: DatasetRole,
                           dataset_creator_class: SupportedDatasetCreator = SupportedDatasetCreator.CLASSIC_TRACE,
                           dataset_creator_params: Dict = None,
                           include_links=True,
                           include_pre_processing: bool = False,
                           pre_processing_steps: List[AbstractDataProcessingStep] = None,
                           **kwargs
                           ) -> Dict[DatasetRole, AbstractDatasetCreator]:
        if not dataset_creator_params:
            dataset_creator_params = deepcopy(BaseTraceTest._DATASET_PARAMS)
        if not include_links:
            dataset_creator_params.pop("true_links")
        if not pre_processing_steps:
            dataset_creator_params["data_cleaner"] = BaseTest.DATA_CLEANER
        if include_pre_processing:
            dataset_creator_params["data_cleaner"] = BaseTest.DATA_CLEANER
        abstract_dataset = dataset_creator_class.value(**dataset_creator_params, **kwargs)
        return {dataset_role: abstract_dataset}

    @staticmethod
    def create(class_type, override=False, **kwargs, ):
        if override:
            args = kwargs
        else:
            args = TestObjectBuilder.get_definition(class_type)
            args.update(kwargs)
        return DefinitionCreator.create(class_type, args)

    @staticmethod
    def get_definition(class_type):
        if class_type in TestObjectBuilder.SUPPORTED_OBJECTS:
            return TestObjectBuilder.SUPPORTED_OBJECTS[class_type]

        raise ValueError("Unable to find definition for:" + class_type)
