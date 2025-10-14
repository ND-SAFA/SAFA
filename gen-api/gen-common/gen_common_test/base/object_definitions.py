from copy import deepcopy
from typing import Dict, Type, TypeVar

from gen_common.constants.dataset_constants import VALIDATION_PERCENTAGE_DEFAULT
from gen_common.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.processing.augmentation.data_augmenter import DataAugmenter
from gen_common.data.readers.api_project_reader import ApiProjectReader
from gen_common.infra.experiment.definition_creator import DefinitionCreator
from gen_common.infra.experiment.variables.typed_definition_variable import TypedDefinitionVariable
from gen_common.llm.args.hugging_face_args import HuggingFaceArgs
from gen_common.llm.model_manager import ModelManager
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_OUTPUT_PATH
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_PRE_TRAIN_PATH
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.test_data.test_data_manager import TestDataManager

ObjectType = TypeVar("ObjectType")


class TestObjectDefinitions:
    DATASET_ARGS_PARAMS = {
        "validation_percentage": VALIDATION_PERCENTAGE_DEFAULT
    }

    augmenter_definition = {"steps":
                                {"*": [[], [{"object_type": "RESAMPLE"}]]}
                            }

    trainer_args_definition = {
        "output_dir": GEN_COMMON_TEST_OUTPUT_PATH,
        "num_train_epochs": 1,
        "metrics": ["classification", "map"]
    }
    job_args_definition = {"output_dir": GEN_COMMON_TEST_OUTPUT_PATH}
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
        "orig_data_path": GEN_COMMON_TEST_PROJECT_PRE_TRAIN_PATH,
        "training_data_dir": GEN_COMMON_TEST_OUTPUT_PATH
    }

    trainer_dataset_manager_definition = {
        "train_dataset_creator": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
            **dataset_creator_definition
        }
    }

    model_manager_definition = {
        "model_path": BaseTest.BASE_TEST_MODEL,
        "model_output_path": GEN_COMMON_TEST_OUTPUT_PATH
    }

    SUPPORTED_OBJECTS = {
        HuggingFaceArgs: trainer_args_definition,
        TraceDatasetCreator: dataset_creator_definition,
        DataAugmenter: augmenter_definition,
        ModelManager: model_manager_definition,
        MLMPreTrainDatasetCreator: pretrain_dataset_definition,
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
            args = TestObjectDefinitions.get_definition(class_type)
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
        if class_type in TestObjectDefinitions.SUPPORTED_OBJECTS:
            return deepcopy(TestObjectDefinitions.SUPPORTED_OBJECTS[class_type])

        raise ValueError("Unable to find definition for:" + class_type)
