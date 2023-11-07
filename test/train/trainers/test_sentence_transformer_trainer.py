from typing import Any, Dict, List
from unittest import TestCase

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.core.args.hugging_face_args import HuggingFaceArgs
from tgen.core.trainers.sentence_transformer_trainer import SentenceTransformerTrainer, SupportedLossFunctions
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.models.model_manager import ModelManager
from tgen.testres.dataset_creator_tutil import DatasetCreatorTUtil
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.test_data_manager import TestDataManager


class TestSentenceTransformerTrainer(TestCase):
    def test_training(self):
        """
        Tests that sentence transformer trainer is able to train and calculates metrics every epoch.
        """
        n_epochs = 2
        trainer = self.create_trainer(trainer_args_kwargs={"num_train_epochs": n_epochs})
        training_output = trainer.perform_training()
        self.assert_valid_metrics(self, training_output.metrics, n_epochs)

    def test_prediction(self):
        """
        Tests that sentence transformer is able to predict.
        """
        trainer = self.create_trainer()
        prediction_output = trainer.perform_prediction(DatasetRole.EVAL)
        scores = prediction_output.predictions
        self.assertEqual(TestDataManager.get_n_candidates(), len(scores))

    def test_loss_functions(self):
        """
        Tests ability to define loss functions on sentence transformer trainer.
        """
        for loss_function in SupportedLossFunctions:
            trainer = self.create_trainer(trainer_args_kwargs={"num_train_epochs": 1}, trainer_kwargs={"loss_function": loss_function})
            training_metrics = trainer.perform_training().metrics
            self.assert_valid_metrics(self, training_metrics, 1)

    @staticmethod
    def assert_valid_metrics(tc: TestCase, metrics: List[Any], n_expected: int) -> None:
        """
        Asserts that metrics have a certain number and that MAP is greater than or equal to 0.5
        :param tc: The test case used to make assertions.
        :param metrics: The metrics being verified.
        :param n_expected: Number of expected metrics.
        :return: None
        """
        tc.assertEqual(n_expected, len(metrics))
        for m in metrics:
            tc.assertGreaterEqual(m["map"], 0.5)

    @staticmethod
    def create_trainer(model_manager_kwargs: Dict = None, trainer_dataset_manager_kwargs: Dict = None,
                       trainer_args_kwargs: Dict = None, trainer_kwargs: Dict = None):
        """
        Creates trainer with given customizations.
        :param model_manager_kwargs: Keyword arguments passed to model manager.
        :param trainer_dataset_manager_kwargs: Keyword arguments passed to trainer dataset manager.
        :param trainer_args_kwargs: Keyword arguments passed to trainer args.
        :param trainer_kwargs: Keyword arguments passed to trainer.
        :return:
        """
        if model_manager_kwargs is None:
            model_manager_kwargs = {}
        if trainer_dataset_manager_kwargs is None:
            trainer_dataset_manager_kwargs = {}
        if trainer_args_kwargs is None:
            trainer_args_kwargs = {}
        if trainer_kwargs is None:
            trainer_kwargs = {}
        model_manager = ModelManager(SMALL_EMBEDDING_MODEL, **model_manager_kwargs)
        trainer_dataset_manager = DatasetCreatorTUtil.create_trainer_dataset_manager(**trainer_dataset_manager_kwargs)
        trainer_args_kwargs = HuggingFaceArgs(TEST_OUTPUT_DIR, **trainer_args_kwargs)
        trainer = SentenceTransformerTrainer(trainer_args_kwargs, model_manager, trainer_dataset_manager, **trainer_kwargs)
        return trainer
