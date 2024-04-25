from copy import deepcopy
from typing import Dict, Type, TypeVar

from tgen.common.constants.dataset_constants import VALIDATION_PERCENTAGE_DEFAULT
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.processing.augmentation.data_augmenter import DataAugmenter
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.experiments.experiment import Experiment
from tgen.experiments.experiment_step import ExperimentStep
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.supported_job_type import SupportedJobType
from tgen.models.model_manager import ModelManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.definition_creator import DefinitionCreator
from tgen.testres.paths.paths import PRETRAIN_DIR, TEST_OUTPUT_DIR
from tgen.testres.test_data_manager import TestDataManager
from tgen.variables.typed_definition_variable import TypedDefinitionVariable

ObjectType = TypeVar("ObjectType")


class ObjectCreator:
    DATASET_ARGS_PARAMS = {
        "validation_percentage": VALIDATION_PERCENTAGE_DEFAULT
    }

    augmenter_definition = {"steps":
                                {"*": [[], [{"object_type": "RESAMPLE"}]]}
                            }

    trainer_args_definition = {
        "output_dir": TEST_OUTPUT_DIR,
        "num_train_epochs": 1,
        "metrics": ["classification", "map"]
    }
    job_args_definition = {"output_dir": TEST_OUTPUT_DIR}
    api_project_reader = {
        "api_definition": {
            "artifacts": TestDataManager.get_artifacts(),
            "layers": TestDataManager.get_path([TestDataManager.Keys.LAYERS]),
            "links": TestDataManager.get_path(TestDataManager.Keys.TRACES)
        }
    }
    dataset_creator_definition = {
        "project_reader": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "API",
            **api_project_reader,
            "overrides": {
                "ALLOWED_ORPHANS": 2
            }
        }
    }

    pretrain_dataset_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "MLM_PRE_TRAIN",
        "orig_data_path": PRETRAIN_DIR,
        "training_data_dir": TEST_OUTPUT_DIR
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
        TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.HUGGING_FACE.name,
        "task": TrainerTask.TRAIN,
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
        TypedDefinitionVariable.OBJECT_TYPE_KEY: SupportedJobType.HUGGING_FACE.name,
        "task": TrainerTask.PREDICT,
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
        HuggingFaceArgs: trainer_args_definition,
        JobArgs: job_args_definition,
        TraceDatasetCreator: dataset_creator_definition,
        TrainerDatasetManager: trainer_dataset_manager_definition,
        DataAugmenter: augmenter_definition,
        ModelManager: model_manager_definition,
        MLMPreTrainDatasetCreator: pretrain_dataset_definition,
        ExperimentStep: experiment_train_step_definition,
        Experiment: experiment_definition,
        ApiProjectReader: api_project_reader
    }

    @staticmethod
    def create(class_type: Type[ObjectType], override=False, **kwargs) -> ObjectType:
        """
        Creates an object of the given type using any additional arguments provided
        :param class_type: The type of object to create
        :param override: Will override default args if True
        :param kwargs: Additional arguments to use for intialization
        :return: The object
        """
        kwargs = deepcopy(kwargs)
        if override:
            args = kwargs
        else:
            args = ObjectCreator.get_definition(class_type)
            args = deepcopy(args)
            args.update(kwargs)
        return DefinitionCreator.create(class_type, args)

    @staticmethod
    def get_definition(class_type: Type[ObjectType]) -> Dict:
        """
        Gets the definition for instantiating an object
        :param class_type: The type of object to get a definition for
        :return: The definition
        """
        if class_type in ObjectCreator.SUPPORTED_OBJECTS:
            return deepcopy(ObjectCreator.SUPPORTED_OBJECTS[class_type])

        raise ValueError("Unable to find definition for:" + class_type)
