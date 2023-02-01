from copy import deepcopy
from typing import Type, TypeVar

from constants import VALIDATION_PERCENTAGE_DEFAULT
from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.processing.augmentation.data_augmenter import DataAugmenter
from experiments.experiment import Experiment
from experiments.experiment_step import ExperimentStep
from jobs.components.job_args import JobArgs
from jobs.supported_job_type import SupportedJobType
from models.model_manager import ModelManager
from testres.base_test import BaseTest
from testres.paths.paths import PRETRAIN_DIR, TEST_OUTPUT_DIR
from testres.test_data_manager import TestDataManager
from train.trainer_args import TrainerArgs
from util.definition_creator import DefinitionCreator
from variables.typed_definition_variable import TypedDefinitionVariable

ObjectType = TypeVar("ObjectType")


class ObjectCreator:
    DATASET_ARGS_PARAMS = {
        "validation_percentage": VALIDATION_PERCENTAGE_DEFAULT
    }

    augmenter_definition = {"steps":
                                {"*": [[], [{"object_type": "SOURCE_TARGET_SWAP"}]]}
                            }

    trainer_args_definition = {
        "output_dir": TEST_OUTPUT_DIR,
        "num_train_epochs": 1,
        "metrics": ["f", "map"]
    }
    job_args_definition = {"output_dir": TEST_OUTPUT_DIR}

    dataset_creator_definition = {
        "project_reader": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "API",
            "api_definition": {
                "source_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE]),
                "target_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET]),
                "true_links": TestDataManager.get_path(TestDataManager.Keys.TRACES)
            }
        }
    }

    pretrain_dataset_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "MLM_PRETRAIN",
        "orig_data_path": PRETRAIN_DIR
    }

    trainer_dataset_manager_definition = {
        "train_dataset_creator": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
            **dataset_creator_definition
        }
    }

    model_manager_definition = {
        "model_path": BaseTest.BASE_TEST_MODEL,
        "model_output_path": TEST_OUTPUT_DIR
    }

    experiment_train_job_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.TRAIN.name,
        "model_manager": model_manager_definition,
        "job_args": {},
        "trainer_dataset_manager": {
            "train_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                "project_reader": {
                    TypedDefinitionVariable.OBJECT_TYPE_KEY: "STRUCTURE",
                    "project_path": {"*": ["path1", "path2"]}
                }
            }
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
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **dataset_creator_definition
            }
        },
        "trainer_args": trainer_args_definition,

    }

    experiment_train_step_definition = {"jobs": [experiment_train_job_definition], "comparison_criterion": {
        "metrics": "accuracy"
    }}
    experiment_predict_step_definition = {"jobs": [experiment_predict_job_definition], "comparison_criterion": {
        "metrics": "accuracy"
    }}
    experiment_definition = {"steps": [experiment_train_step_definition, experiment_predict_step_definition],
                             "output_dir": TEST_OUTPUT_DIR}

    SUPPORTED_OBJECTS = {
        TrainerArgs: trainer_args_definition,
        JobArgs: job_args_definition,
        TraceDatasetCreator: dataset_creator_definition,
        TrainerDatasetManager: trainer_dataset_manager_definition,
        DataAugmenter: augmenter_definition,
        ModelManager: model_manager_definition,
        MLMPreTrainDatasetCreator: pretrain_dataset_definition,
        ExperimentStep: experiment_train_step_definition,
        Experiment: experiment_definition
    }

    @staticmethod
    def create(class_type: Type[ObjectType], override=False, **kwargs) -> ObjectType:
        kwargs = deepcopy(kwargs)
        if override:
            args = kwargs
        else:
            args = ObjectCreator.get_definition(class_type)
            args = deepcopy(args)
            args.update(kwargs)
        return DefinitionCreator.create(class_type, args)

    @staticmethod
    def get_definition(class_type):
        if class_type in ObjectCreator.SUPPORTED_OBJECTS:
            return deepcopy(ObjectCreator.SUPPORTED_OBJECTS[class_type])

        raise ValueError("Unable to find definition for:" + class_type)
