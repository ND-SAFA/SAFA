from typing import Any

from tracer.models.model_generator import ModelGenerator


class AbstractDataset:

    def to_trainer_dataset(self, model_generator: ModelGenerator) -> Any:
        """
        Converts datasets to that used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A datasets used by the HF trainer.
        """
