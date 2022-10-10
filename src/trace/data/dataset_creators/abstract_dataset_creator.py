from abc import abstractmethod, ABC

from trace.data.dataset import Dataset


class AbstractDatasetCreator(ABC):
    """
    Responsible for creating dataset in format for defined models.
    """

    @abstractmethod
    def get_dataset(self) -> Dataset:
        """
        Gets the dataset
        :return: the dataset
        """
        pass
