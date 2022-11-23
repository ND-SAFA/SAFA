from typing import Optional

from config.constants import RESAMPLE_RATE_DEFAULT, VALIDATION_PERCENTAGE_DEFAULT
from tracer.datasets.abstract_dataset import AbstractDataset
from tracer.datasets.dataset_role import DatasetRole
from tracer.datasets.pre_train_dataset import PreTrainDataset
from tracer.datasets.trace_dataset import TraceDataset


class TrainerDatasetsContainer:

    def __init__(self,
                 pre_train: PreTrainDataset = None,
                 train: AbstractDataset = None,
                 val: AbstractDataset = None,
                 eval: TraceDataset = None,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT, split_train_dataset: bool = False,
                 resample_rate: int = RESAMPLE_RATE_DEFAULT
                 ):
        """
        Container to hold all the datasets used in the TraceTrainer
        :param pre_train: The pre-training dataset creator.
        :param train: The training dataset creator.
        :param val: the validation dataset creator.
        :param eval: The training dataset creator.
        :param validation_percentage: percentage of the data to use for validation datasets
        :param split_train_dataset: if True, splits the training datasets into a train, val datasets
        :param resample_rate: the rate at which to resample positive examples in the train datasets
        """
        self.pre_train_dataset: Optional[PreTrainDataset] = pre_train
        self.train_dataset: Optional[AbstractDataset] = train
        self.val_dataset: Optional[AbstractDataset] = val
        self.eval_dataset: Optional[TraceDataset] = eval
        if isinstance(self.train_dataset, TraceDataset) and split_train_dataset:
            self.train_dataset, self.val_dataset = self.train_dataset.train_test_split(validation_percentage,
                                                                                       resample_rate)

    def save_dataset_splits(self, output_dir: str) -> None:
        """
        Saves all dataset splits to the output dir
        :param output_dir: directory to save to
        :return: None
        """
        for dataset_role in DatasetRole:
            if dataset_role in self:
                self[dataset_role].save(output_dir, dataset_role.name.lower())

    def __getitem__(self, dataset_role: DatasetRole) -> AbstractDataset:
        """
        Returns the datasets corresponding to role.
        :param dataset_role: The role of the datasets returned.
        :return: PreTrainDataset if pretrain role otherwise TraceDataset
        """
        self.__assert_index(dataset_role)
        if dataset_role == DatasetRole.TRAIN:
            return self.train_dataset
        elif dataset_role == DatasetRole.PRE_TRAIN:
            return self.pre_train_dataset
        elif dataset_role == DatasetRole.EVAL:
            return self.eval_dataset
        elif dataset_role == DatasetRole.VAL:
            return self.val_dataset
        else:
            raise Exception("Not datasets found corresponding with:" + str(dataset_role))

    def __setitem__(self, dataset_role: DatasetRole, dataset: AbstractDataset):
        """
        Sets given datasets for given attribute corresponding to role
        :param dataset_role: The role defining attribute to set
        :param dataset: The datasets to set
        :return: None
        """
        self.__assert_index(dataset_role)
        if dataset_role == DatasetRole.TRAIN:
            self.train_dataset = dataset
        elif dataset_role == DatasetRole.PRE_TRAIN:
            self.pre_train_dataset = dataset
        elif dataset_role == DatasetRole.EVAL:
            self.eval_dataset = dataset
        elif dataset_role == DatasetRole.VAL:
            self.val_dataset = dataset
        else:
            raise Exception("Not datasets found corresponding with:" + str(dataset_role))

    def __contains__(self, dataset_role: DatasetRole):
        """
        Returns whether datasets exists for given role
        :param dataset_role: The role to check a datasets for.
        :return: Boolean representing whether datasets exists for role
        """
        return self[dataset_role] is not None

    def __assert_index(self, index_value):
        if not isinstance(index_value, DatasetRole):
            raise Exception("Expected index to be datasets role:" + index_value)

    def __repr__(self):
        return str({role.name: type(self[role]) for role in DatasetRole})
