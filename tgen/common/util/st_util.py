from typing import List, Tuple

from datasets import Dataset
from sentence_transformers import InputExample, SentenceTransformer

from tgen.common.constants.hugging_face_constants import NEG_LINK
from tgen.common.logging.logger_manager import logger
from tgen.common.util.list_util import ListUtil
from tgen.data.keys.csv_keys import CSVKeys
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager


class STUtil:
    @staticmethod
    def to_input_examples(dataset: Dataset, use_scores: bool = False, model: SentenceTransformer = None) -> List[InputExample]:
        """
        Converts a huggingface dataset into a list of sentence transformer input examples.
        :param dataset: The huggingface dataset.
        :param use_scores: Whether to use score over label for negative links.
        :param model: If use_scores, the model used to embed artifacts.
        :return: List of input examples.
        """
        input_examples = []
        for i in dataset:
            source_text = i[CSVKeys.SOURCE]
            target_text = i[CSVKeys.TARGET]
            label = float(i[CSVKeys.LABEL])
            score = i.get(CSVKeys.SCORE, None)
            if use_scores and score:
                label = float(score)
            input_examples.append(InputExample(texts=[source_text, target_text], label=label))

        if use_scores and all([i.label is None for i in input_examples]):
            assert model, f"Model is required to be defined if use_scores is True. Received {model}."
            STUtil.replace_labels_with_scores(model, input_examples)
        return input_examples

    @staticmethod
    def replace_labels_with_scores(model: SentenceTransformer, input_examples: List[InputExample], label: int = NEG_LINK):
        """
        Replaces the matching labels with model similarity score.
        :param model: The model to create embeddings for artifacts for.
        :param input_examples: The input examples to modify.
        :param label: The label to replace with scores.
        :return: None. Modified in place.
        """
        examples_with_label = [input_example for input_example in input_examples if input_example.label == label]
        content = ListUtil.flatten([input_example.texts for input_example in examples_with_label])

        embeddings_manager = EmbeddingsManager.create_from_content(content, model=model, show_progress_bar=False)

        for input_example in examples_with_label:
            input_example.label = STUtil.get_input_example_score(embeddings_manager, input_example)

        logger.info(f"Adding scores to {len(examples_with_label)} input examples.")

    @staticmethod
    def get_input_example_score(embeddings_manager: EmbeddingsManager, input_example: InputExample) -> float:
        """
        Calculates the similarity score between the two texts in the input example.
        :param embeddings_manager: The embeddings manager containing embedding to text.
        :param input_example: The input example containing texts to compare.
        :return: The similarity score between texts.
        """
        s_text, t_text = input_example.texts
        s_embedding = embeddings_manager.get_embedding(s_text)
        t_embedding = embeddings_manager.get_embedding(t_text)

        score = embeddings_manager.compare_artifact(s_text, t_text)
        return score

    @staticmethod
    def calculate_similarities(model: SentenceTransformer, input_examples: List[InputExample]) -> Tuple[List[float], List[float]]:
        """
        Calculates the cosine similarity between the texts in each input example. TODO: Replace with embedding util.
        :param model: The model used to embed the test dataset.
        :param input_examples: The list of input examples to calculate similarities for.
        :return: Prediction output containing scores as predictions and labels as label ids.
        """
        unique_content = ListUtil.flatten([e.texts for e in input_examples])
        embeddings_manager = EmbeddingsManager.create_from_content(unique_content, model=model, show_progress_bar=False)
        scores = []
        labels = []
        for example in input_examples:
            score = STUtil.get_input_example_score(embeddings_manager, example)
            scores.append(score)
            labels.append(example.label)
        return scores, labels
