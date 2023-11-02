from typing import List, Optional

from datasets import Dataset
from sentence_transformers import InputExample, losses
from sklearn.metrics.pairwise import cosine_similarity
from torch.utils.data import DataLoader
from transformers.trainer_utils import PredictionOutput

from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.data.tdatasets.dataset_role import DatasetRole


class SentenceTransformerTrainer(HuggingFaceTrainer):
    """
    Trains sentence transformer models. They have a slightly modified API for training the models and loading the data.
    """

    def predict(
            self, test_dataset: List[InputExample], ignore_keys: Optional[List[str]] = None, metric_key_prefix: str = "test"
    ) -> PredictionOutput:
        embeddings = {}

        def encode(batch: List[str]):
            batch_embeddings = self.model.encode(batch)
            for k, v in zip(batch, batch_embeddings):
                embeddings[k] = v

        unique_texts = set([a for e in test_dataset for a in e.texts])
        encode(list(unique_texts))

        scores = []
        labels = []
        for example in test_dataset:
            source_text, target_text = example.texts
            source_embedding = embeddings[source_text]
            target_embedding = embeddings[target_text]
            score = cosine_similarity([source_embedding], [target_embedding])[0][0]
            scores.append(score)
            labels.append(example.label)
        return PredictionOutput(predictions=scores, label_ids=labels, metrics={})

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
