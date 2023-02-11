import os
from typing import Dict
from unittest import mock

from constants import BEST_MODEL_NAME
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest
from train.kal_trainer import KalTrainer
from train.trainer_args import TrainerArgs
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestKalTrainer(BaseTraceTest):

    def test_save_checkpoint(self):
        test_trace_trainer = self.get_custom_trace_trainer()
        test_trace_trainer.perform_training()
        checkpoint_files = ["optimizer.bin", "config.json", "pytorch_model.bin", "scheduler.bin",
                            "training_args.bin"]
        for folder_name in [BEST_MODEL_NAME, KalTrainer.CURRENT_MODEL_NAME]:
            folder_path = os.path.join(test_trace_trainer.trainer_args.output_dir, folder_name)
            output_files = list(os.listdir(folder_path))
            for file in checkpoint_files:
                self.assertIn(file, output_files)

    @staticmethod
    def create_trainer_dataset_manager(kwargs: Dict = None) -> TrainerDatasetManager:
        """
        Creates dataset manager with optional kwargs used to modify definition.
        :param kwargs: Dictionary of properties to overwrite in dataset manager definition.
        :return: Dataset manager created.
        """
        if kwargs is None:
            kwargs = {}
        return ObjectCreator.create(TrainerDatasetManager, **{
            "eval_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            },
            "val_dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
                "val_percentage": .3
            },
            **kwargs
        })

    def get_custom_trace_trainer(self, dataset_container_args: Dict = None, **kwargs):
        trainer_dataset_manager = self.create_trainer_dataset_manager(dataset_container_args)
        model_manager = ObjectCreator.create(ModelManager)
        model_manager.get_model = mock.MagicMock(return_value=self.get_test_model())
        model_manager.get_tokenizer = mock.MagicMock(return_value=self.get_test_tokenizer())
        model_manager.get_config = mock.MagicMock(return_value=self.get_test_config())
        trainer_args = ObjectCreator.create(TrainerArgs, **kwargs)
        return KalTrainer(
            trainer_args=trainer_args,
            trainer_dataset_manager=trainer_dataset_manager,
            model_manager=model_manager)
