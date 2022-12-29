from copy import deepcopy
from typing import Dict, List, Type, TypeVar

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from data.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.datasets.creators.split_dataset_creator import SplitDatasetCreator
from data.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from data.datasets.dataset_role import DatasetRole
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from experiments.experiment import Experiment
from experiments.experiment_step import ExperimentStep
from jobs.components.job_args import JobArgs
from jobs.supported_job_type import SupportedJobType
from models.model_manager import ModelManager
from test.base_test import BaseTest
from test.base_trace_test import BaseTraceTest
from test.definition_creator import DefinitionCreator
from test.paths.paths import PRETRAIN_DIR, TEST_OUTPUT_DIR
from test.test_data_manager import TestDataManager
from train.trainer_args import TrainerArgs
from util.variables.typed_definition_variable import TypedDefinitionVariable

ObjectType = TypeVar("ObjectType")


class TestObjectCreator:
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
        "source_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE]),
        "target_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET]),
        "true_links": TestDataManager.get_path(TestDataManager.Keys.TRACES)
    }

    pretrain_dataset_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "MLM_PRETRAIN",
        "orig_data_path": PRETRAIN_DIR
    }

    trainer_dataset_manager_definition = {
        "train_dataset_creator": {TypedDefinitionVariable.OBJECT_TYPE_KEY: "CLASSIC_TRACE",
                                  **dataset_creator_definition}
    }

    model_manager_definition = {
        "model_path": "bert-base-uncased",
        "model_output_path": TEST_OUTPUT_DIR
    }

    experiment_train_job_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.TRAIN.name,
        "model_manager": model_manager_definition,
        "job_args": {},
        "trainer_dataset_manager": {
            "train_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "Safa",
                "project_path": {"*": ["path1", "path2"]}}
        },
        "trainer_args": {
            "output_dir": TEST_OUTPUT_DIR,
            "num_train_epochs": {"*": [100, 200]}
        }
    }

    experiment_predict_job_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.PREDICT.name,
        "model_manager": model_manager_definition,
        "job_args": {},
        "trainer_dataset_manager": {
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "CLASSIC_TRACE",
                **dataset_creator_definition
            }
        },
        "trainer_args": trainer_args_definition,

    }

    experiment_train_step_definition = {"jobs": [experiment_train_job_definition], "comparison_metric": "accuracy"}
    experiment_predict_step_definition = {"jobs": [experiment_predict_job_definition], "comparison_metric": "accuracy"}
    experiment_definition = {"steps": [experiment_train_step_definition, experiment_predict_step_definition],
                             "output_dir": TEST_OUTPUT_DIR}

    SUPPORTED_OBJECTS = {
        TrainerArgs: trainer_args_definition,
        JobArgs: job_args_definition,
        ClassicTraceDatasetCreator: dataset_creator_definition,
        TrainerDatasetManager: trainer_dataset_manager_definition,
        ModelManager: model_manager_definition,
        MLMPreTrainDatasetCreator: pretrain_dataset_definition,
        ExperimentStep: experiment_train_step_definition,
        Experiment: experiment_definition
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
    def create(class_type: Type[ObjectType], override=False, **kwargs) -> ObjectType:
        kwargs = deepcopy(kwargs)
        if override:
            args = kwargs
        else:
            args = TestObjectCreator.get_definition(class_type)
            args = deepcopy(args)
            args.update(kwargs)
        return DefinitionCreator.create(class_type, args)

    @staticmethod
    def get_definition(class_type):
        if class_type in TestObjectCreator.SUPPORTED_OBJECTS:
            return deepcopy(TestObjectCreator.SUPPORTED_OBJECTS[class_type])

        raise ValueError("Unable to find definition for:" + class_type)
