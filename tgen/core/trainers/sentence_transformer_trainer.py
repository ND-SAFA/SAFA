from typing import Optional

from datasets import Dataset
from sentence_transformers import losses
from torch.utils.data import DataLoader

from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.data.tdatasets.dataset_role import DatasetRole


class SentenceTransformerTrainer(HuggingFaceTrainer):
    """
    Trains sentence transformer models. They have a slightly modified API for training the models and loading the data.
    """

    def train(
            self,
            **kwargs,
    ) -> None:
        """
        Trains a sentence transformer model.
        :param kwargs: Currently ignored. TODO: add ability to start from checkpoint.
        :return: None
        """
        train_dataloader = DataLoader(self.train_dataset, shuffle=True, batch_size=self.args.train_batch_size)
        train_loss = losses.CosineSimilarityLoss(self.model)
        self.model.fit(train_objectives=[(train_dataloader, train_loss)],
                       epochs=self.args.num_train_epochs,
                       warmup_steps=self.args.warmup_steps)

    def _get_dataset(self, dataset_role: DatasetRole) -> Optional[Dataset]:
        return self.trainer_dataset_manager[dataset_role].to_trainer_dataset(self.model_manager)
