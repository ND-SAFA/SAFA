from typing import List, Optional, Union, Dict

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from tracer.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.datasets.pre_train_dataset import PreTrainDataset
from tracer.datasets.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from tracer.datasets.trace_dataset import TraceDataset


class TrainerDatasetsContainer:
    def __init__(self,
                 pre_train: AbstractDatasetCreator = None,
                 train: AbstractDatasetCreator = None,
                 val: AbstractDatasetCreator = None,
                 eval: AbstractDatasetCreator = None,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT, split_train_dataset: bool = False,
                 augmentation_steps: List[AbstractDataAugmentationStep] = None
                 ):
        """
        Container to hold all the datasets used in the TraceTrainer
        :param pre_train: The pre-training dataset creator.
        :param train: The training dataset creator.
        :param val: the validation dataset creator.
        :param eval: The training dataset creator.
        :param validation_percentage: percentage of the data to use for validation datasets
        :param split_train_dataset: if True, splits the training datasets into a train, val datasets
        :param augmentation_steps: steps to run to augment the training data
        """
        self.__pre_train_creator = pre_train
        self.__train_creator = train
        self.__val_creator = val
        self.__eval_creator = eval
        self.__pre_train_dataset: Optional[PreTrainDataset] = self.__optional_create(pre_train)
        self.__train_dataset: Optional[TraceDataset] = self.__optional_create(train)
        self.__val_dataset: Optional[TraceDataset] = self.__optional_create(val)
        self.__eval_dataset: Optional[TraceDataset] = self.__optional_create(eval)

        if isinstance(self.__train_dataset, TraceDataset):
            if split_train_dataset:
                self.train_dataset, self.val_dataset = self.__train_dataset.split(validation_percentage)
            self.train_dataset.prepare_for_training(augmentation_steps)

    def get_creator(self, dataset_role: DatasetRole):
        if dataset_role == DatasetRole.PRE_TRAIN:
            return self.__pre_train_creator
        if dataset_role == DatasetRole.TRAIN:
            return self.__train_creator
        if dataset_role == DatasetRole.VAL:
            return self.__val_creator
        if dataset_role == DatasetRole.EVAL:
            return self.__eval_creator
        raise Exception("Unrecognized role:" + dataset_role.name)

    @staticmethod
    def create_from_map(dataset_map: Dict[DatasetRole, AbstractDatasetCreator], **kwargs):
        """
        Creates instance containing dataset for each mapped role.
        :param dataset_map: The map of roles to datasets to set in instance.
        :param kwargs: Additional initialization parameters to instance.
        :return: TrainerDatasetsContainer with initialized datasets.
        """
        trainer_datasets_container = TrainerDatasetsContainer(**kwargs)
        for dataset_role, dataset_creator in dataset_map.items():
            trainer_datasets_container[dataset_role] = dataset_creator.create()
        return trainer_datasets_container

    def save_dataset_splits(self, output_dir: str) -> None:
        """
        Saves all dataset splits to the output dir
        :param output_dir: directory to save to
        :return: None
        """
        for dataset_role in DatasetRole:
            if dataset_role in self:
                self[dataset_role].save(output_dir, dataset_role.name.lower())

    def __getitem__(self, dataset_role: DatasetRole) -> Optional[Union[TraceDataset, PreTrainDataset]]:
        """
        Returns the datasets corresponding to role.
        :param dataset_role: The role of the datasets returned.
        :return: PreTrainDataset if pretrain role otherwise TraceDataset
        """

        self.__assert_index(dataset_role)
        if dataset_role == DatasetRole.TRAIN:
            return self.__train_dataset
        elif dataset_role == DatasetRole.PRE_TRAIN:
            return self.__pre_train_dataset
        elif dataset_role == DatasetRole.EVAL:
            return self.__eval_dataset
        elif dataset_role == DatasetRole.VAL:
            return self.__val_dataset
        else:
            raise Exception("Not datasets found corresponding with:" + str(dataset_role))

    @staticmethod
    def __optional_create(dataset_creator: Optional[AbstractDatasetCreator]) -> Optional[Union[TraceDataset, PreTrainDataset]]:
        """
        Creates dataset set if not None, otherwise None is returned.
        :param dataset_creator: The optional dataset creator to use.
        :return: None or Dataset
        """
        return None if dataset_creator is None else dataset_creator.create()

    def __setitem__(self, dataset_role: DatasetRole, dataset: Union[TraceDataset, PreTrainDataset]):
        """
        Sets given datasets for given attribute corresponding to role
        :param dataset_role: The role defining attribute to set
        :param dataset: The datasets to set
        :return: None
        """
        self.__assert_index(dataset_role)
        if dataset_role == DatasetRole.TRAIN:
            self.__train_dataset = dataset
        elif dataset_role == DatasetRole.PRE_TRAIN:
            self.__pre_train_dataset = dataset
        elif dataset_role == DatasetRole.EVAL:
            self.__eval_dataset = dataset
        elif dataset_role == DatasetRole.VAL:
            self.__val_dataset = dataset
        else:
            raise Exception("Not datasets found corresponding with:" + str(dataset_role))

    def __contains__(self, dataset_role: DatasetRole):
        """
        Returns whether datasets exist for given role.
        :param dataset_role: The role to check a datasets for.
        :return: Boolean representing whether datasets exist for role
        """
        return self[dataset_role] is not None

    @staticmethod
    def __assert_index(index_value):
        """
        Asserts that value is instance of DatasetRole
        :param index_value: The value expected to be dataset role.
        :return: None
        """
        if not isinstance(index_value, DatasetRole):
            raise Exception("Expected index to be datasets role:" + index_value)

    def __repr__(self):
        """
        Returns string representation of role to type of mapped dataset.
        :return: String representation of trainer datasets container.
        """
        return str({role.name: type(self[role]) for role in DatasetRole})
