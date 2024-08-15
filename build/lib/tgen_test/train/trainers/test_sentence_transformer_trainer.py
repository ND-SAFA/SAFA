import os
from typing import Dict, List
from unittest import TestCase, skip

import numpy as np
from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.llm.args.hugging_face_args import HuggingFaceArgs
from common_resources.tools.constants.hugging_face_constants import POS_LINK, SMALL_EMBEDDING_MODEL

from tgen.core.trainers.st_embedding_trainer import STEmbeddingTrainer, STTrainer
from tgen.core.trainers.st_loss_functions import SupportedSTLossFunctions
from tgen.models.model_manager import ModelManager
from tgen.testres.dataset_creator_tutil import DatasetCreatorTUtil
from tgen.testres.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from tgen.testres.test_data_manager import TestDataManager


# TODO: Find why tests are finicky

class TestSTTrainer(TestCase):
    @skip
    def test_training(self):
        """
        Tests that sentence transformer trainer is able to train and calculates metrics every epoch.
        """
        n_epochs = 2
        trainer = self.create_trainer(trainer_args_kwargs={"num_train_epochs": n_epochs})
        training_metrics = trainer.perform_training().metrics
        self.verify_training_metrics(self, training_metrics, n_epochs)

    @skip
    def test_prediction(self):
        """
        Tests that sentence transformer is able to predict.
        """
        trainer = self.create_trainer()
        prediction_output = trainer.perform_prediction(DatasetRole.EVAL)
        scores = prediction_output.predictions
        self.assertEqual(TestDataManager.get_n_candidates(), len(scores))

    @skip
    def test_loss_functions(self):
        """
        Tests ability to define loss functions on sentence transformer trainer.
        """
        for loss_function in SupportedSTLossFunctions:
            trainer = self.create_trainer(trainer_args_kwargs={"num_train_epochs": 1, "st_loss_function": loss_function.name})
            training_metrics = trainer.perform_training().metrics
            self.verify_training_metrics(self, training_metrics, 1, msg=f"Loss function: {loss_function}")

    @skip
    def test_zero_loss(self) -> None:
        """
        Tests that there is zero loss for negative links.
        """
        trainer = self.create_trainer(trainer_args_kwargs={"train_batch_size": 2, "shuffle": False, "use_scores": True},
                                      # shuffle allows constant pos indices
                                      trainer_dataset_manager_kwargs=self.get_cat_dataset_definition())
        self.assertTrue(trainer.trainer_args.use_scores)

        train_dataset = trainer.trainer_dataset_manager[DatasetRole.TRAIN]
        link_ids = train_dataset.get_ordered_link_ids()
        pos_link_indices = [i for i, link_id in enumerate(link_ids) if
                            train_dataset.trace_df.get_link(link_id)[TraceKeys.LABEL] == POS_LINK]

        train_metrics = trainer.perform_training().metrics
        train_losses = [m["loss"] for m in train_metrics]
        max_loss_index = np.argmax(train_losses)
        self.assertIn(max_loss_index, pos_link_indices)  # indices of positive labels.

    @staticmethod
    def create_trainer(model_manager_kwargs: Dict = None, trainer_dataset_manager_kwargs: Dict = None,
                       trainer_args_kwargs: Dict = None, trainer_kwargs: Dict = None,
                       save_best_model: bool = False) -> STTrainer:
        """
        Creates trainer with given customizations.
        :param model_manager_kwargs: Keyword arguments passed to model manager.
        :param trainer_dataset_manager_kwargs: Keyword arguments passed to trainer dataset manager.
        :param trainer_args_kwargs: Keyword arguments passed to trainer args.
        :param trainer_kwargs: Keyword arguments passed to trainer.
        :param save_best_model: Whether to save the best model
        :return: Sentence transformer trainer.
        """
        if model_manager_kwargs is None:
            model_manager_kwargs = {}
        if trainer_dataset_manager_kwargs is None:
            trainer_dataset_manager_kwargs = {}
        if trainer_args_kwargs is None:
            trainer_args_kwargs = {}
        if trainer_kwargs is None:
            trainer_kwargs = {}

        trainer_args_kwargs["save_best_model"] = save_best_model

        model_manager = ModelManager(SMALL_EMBEDDING_MODEL, **model_manager_kwargs)
        trainer_dataset_manager = DatasetCreatorTUtil.create_trainer_dataset_manager(val_percentage=0.4,
                                                                                     **trainer_dataset_manager_kwargs)
        trainer_args_kwargs = HuggingFaceArgs(TEST_OUTPUT_DIR, **trainer_args_kwargs)
        trainer = STEmbeddingTrainer(trainer_args_kwargs, model_manager, trainer_dataset_manager, **trainer_kwargs)
        return trainer

    @staticmethod
    def verify_training_metrics(tc: TestCase, metrics: List[Dict], n_expected: int, **kwargs) -> None:
        """
        Asserts that metrics have a certain number and that MAP is greater than or equal to 0.5
        :param tc: The test case used to make assertions.
        :param metrics: The metrics being verified.
        :param n_expected: Number of expected metrics.
        :return: None
        """
        tc.assertEqual(n_expected, len(metrics))
        for metric in metrics:
            tc.assertGreater(metric["loss"], 0, **kwargs)

    @staticmethod
    def get_cat_dataset_definition():
        """
        :return: The definition of the Cats dataset.
        """
        return {
            "additional_roles": [],
            "train_dataset_creator": {
                "object_type": "TRACE",
                "project_reader": {
                    "object_type": "STRUCTURE",
                    "project_path": os.path.join(TEST_DATA_DIR, "cats")
                }
            },
            "val_dataset_creator": {
                "object_type": "SPLIT",
                "val_percentage": 0.33,
                "split_strategy": "SPLIT_BY_LINK"
            }
        }
