from dataclasses import dataclass
from typing import Union

from tracer.dataset.dataset_role import DatasetRole
from tracer.dataset.pre_train_dataset import PreTrainDataset
from tracer.dataset.trace_dataset import TraceDataset


@dataclass
class DatasetMap:
    pre_train_dataset: PreTrainDataset = None
    train_dataset: TraceDataset = None
    eval_dataset: TraceDataset = None

    def __getitem__(self, dataset_role: DatasetRole) -> Union[PreTrainDataset, TraceDataset]:
        """
        Returns the dataset corresponding to role.
        :param dataset_role: The role of the dataset returned.
        :return: PreTrainDataset if pretrain role otherwise TraceDataset
        """
        self.__assert_index(dataset_role)
        if dataset_role == DatasetRole.TRAIN:
            return self.train_dataset
        elif dataset_role == DatasetRole.PRE_TRAIN:
            return self.pre_train_dataset
        elif dataset_role == DatasetRole.EVAL:
            return self.eval_dataset
        else:
            raise Exception("Not dataset found corresponding with:" + str(dataset_role))

    def __setitem__(self, dataset_role: DatasetRole, dataset: Union[PreTrainDataset, TraceDataset]):
        """
        Sets given dataset for given attribute corresponding to role
        :param dataset_role: The role defining attribute to set
        :param dataset: The dataset to set
        :return: None
        """
        self.__assert_index(dataset_role)
        if dataset_role == DatasetRole.TRAIN:
            self.train_dataset = dataset
        elif dataset_role == DatasetRole.PRE_TRAIN:
            self.pre_train_dataset = dataset
        elif dataset_role == DatasetRole.EVAL:
            self.eval_dataset = dataset
        else:
            raise Exception("Not dataset found corresponding with:" + str(dataset_role))

    def __contains__(self, dataset_role: DatasetRole):
        """
        Returns whether dataset exists for given role
        :param dataset_role: The role to check a dataset for.
        :return: Boolean representing whether dataset exists for role
        """
        return self[dataset_role] is not None

    def __assert_index(self, index_value):
        if not isinstance(index_value, DatasetRole):
            raise Exception("Expected index to be dataset role:" + index_value)
