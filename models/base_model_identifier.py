from abc import abstractmethod
from transformers.modeling_utils import PreTrainedModel


class BaseModelIdentifier:

    @abstractmethod
    @property
    def model_class(self) -> PreTrainedModel:
        pass

    @abstractmethod
    @property
    def model_path(self) -> str:
        pass
