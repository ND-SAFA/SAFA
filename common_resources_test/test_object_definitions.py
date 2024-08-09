from copy import deepcopy
from typing import Dict, Type, TypeVar

from common_resources.tools.constants.dataset_constants import VALIDATION_PERCENTAGE_DEFAULT
from common_resources.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.processing.augmentation.data_augmenter import DataAugmenter
from common_resources.data.readers.api_project_reader import ApiProjectReader
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.llm.model_manager import ModelManager
from common_resources.tools.variables.typed_definition_variable import TypedDefinitionVariable
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.definition_creator import DefinitionCreator
from common_resources_test.paths.base_paths import TEST_OUTPUT_DIR, PRETRAIN_DIR
from common_resources_test.test_data.test_data_manager import TestDataManager

ObjectType = TypeVar("ObjectType")


class TestObjectDefinitions:
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
