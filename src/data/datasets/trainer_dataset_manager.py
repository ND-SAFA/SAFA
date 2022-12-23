from collections import OrderedDict
from typing import Dict, List, Optional, Union, Type, Any

from config.override import overrides
from data.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.creators.split_dataset_creator import SplitDatasetCreator
from data.creators.supported_dataset_creator import SupportedDatasetCreator
from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.dataset_role import DatasetRole
from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.trace_dataset import TraceDataset
from data.processing.augmentation.data_augmenter import DataAugmenter
from experiments.variables.definition_variable import DefinitionVariable
from util.base_object import BaseObject


class TrainerDatasetManager(BaseObject):
    DATASET_TYPE = Union[PreTrainDataset, TraceDataset, AbstractDataset]

    def __init__(self,
                 pre_train_dataset_creator: AbstractDatasetCreator = None,
                 train_dataset_creator: AbstractDatasetCreator = None,
                 val_dataset_creator: AbstractDatasetCreator = None,
                 eval_dataset_creator: AbstractDatasetCreator = None,
                 augmenter: DataAugmenter = None
                 ):
        """
        Container to hold all the data used in the TraceTrainer
        :param pre_train_dataset_creator: The pre-training dataset creator.
        :param train_dataset_creator: The training dataset creator.
        :param val_dataset_creator: the validation dataset creator.
        :param eval_dataset_creator: The training dataset creator.data
        :param augmenter: augmenter to use for augmenting datasets
        """
        self.__dataset_creators = {DatasetRole.PRE_TRAIN: pre_train_dataset_creator,
                                   DatasetRole.TRAIN: train_dataset_creator,
                                   DatasetRole.VAL: val_dataset_creator, DatasetRole.EVAL: eval_dataset_creator}
        self.__datasets = self._create_datasets_from_creators(self.__dataset_creators)
        self._prepare_datasets(augmenter)

    def get_creator(self, dataset_role: DatasetRole) -> AbstractDatasetCreator:
        """
        Gets the dataset creator for the given role
        :param dataset_role: the dataset role
        :return: the dataset creator for the given role
        """
        return self.__dataset_creators[dataset_role]

    def save_dataset_splits(self, output_dir: str) -> List[str]:
        """
        Saves all dataset splits to the output dir
        :param output_dir: directory to save to
        :return: the list of files that were saved
        """
        output_paths = []
        for dataset_role in DatasetRole:
            if dataset_role in self:
                output_path = self[dataset_role].save(output_dir, dataset_role.name.lower())
                output_paths.append(output_path)
        return output_paths

    @staticmethod
    def create_from_map(dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]):
        """
        Creates instance containing dataset for each mapped role.
        :param dataset_creators_map: The map of roles to data to set in instance.
        :return: TrainerDatasetManager with initialized data.
        """
        trainer_datasets_container = TrainerDatasetManager(
            pre_train_dataset_creator=dataset_creators_map.get(DatasetRole.PRE_TRAIN, None),
            train_dataset_creator=dataset_creators_map.get(DatasetRole.TRAIN, None),
            val_dataset_creator=dataset_creators_map.get(DatasetRole.VAL, None),
            eval_dataset_creator=dataset_creators_map.get(DatasetRole.EVAL, None))
        return trainer_datasets_container

    @classmethod
    @overrides(BaseObject)
    def _get_expected_class_for_abstract(cls, abstract_class: Type, child_class_name: str) -> Any:
        """
        Returns the correct expected class when given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the expected type
        """
        return SupportedDatasetCreator[child_class_name.upper()]

    def _prepare_datasets(self, data_augmenter: DataAugmenter) -> None:
        """
        Performs any necessary additional steps necessary to prepare each dataset
        :param data_augmenter: The augmenter responsible for generating new positive samples.
        :return: None
        """
        train_dataset = self[DatasetRole.TRAIN]
        if isinstance(self[DatasetRole.TRAIN], TraceDataset):
            dataset_splits_map = self._create_dataset_splits(train_dataset, self.__dataset_creators)
            self.__datasets.update(dataset_splits_map)
            self[DatasetRole.TRAIN].prepare_for_training(data_augmenter)

    @staticmethod
    def _create_dataset_splits(train_dataset: TraceDataset,
                               dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) \
            -> Dict[DatasetRole, TraceDataset]:
        """
        Splits the train dataset into desired splits and creates a dictionary mapping dataset role to split for all split data
        :param train_dataset: the train dataset
        :param dataset_creators_map: a map of dataset role to all dataset creators
        :return: a dictionary mapping dataset role to split for all split data
        """
        dataset_percent_splits = OrderedDict({dataset_role: dataset_creator.split_percentage
                                              for dataset_role, dataset_creator in dataset_creators_map.items()
                                              if isinstance(dataset_creator, SplitDatasetCreator)})
        dataset_splits_map = {}
        if len(dataset_percent_splits) < 1:
            return dataset_splits_map
        splits = train_dataset.split_multiple(list(dataset_percent_splits.values()))
        train_dataset, split_datasets = splits[0], splits[1:]
        dataset_splits_map[DatasetRole.TRAIN] = train_dataset
        for i, dataset_role in enumerate(dataset_percent_splits.keys()):
            dataset_splits_map[dataset_role] = split_datasets[i]
        return dataset_splits_map

    @staticmethod
    def _create_datasets_from_creators(dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) \
            -> Dict[DatasetRole, DATASET_TYPE]:
        """
        Creates the data from their corresponding creators
        :return: a dictionary mapping dataset role to the corresponding dataset
        """
        return {dataset_role: TrainerDatasetManager.__optional_create(dataset_creator)
                for dataset_role, dataset_creator in dataset_creators_map.items()}

    @staticmethod
    def __optional_create(dataset_creator: Optional[AbstractDatasetCreator]) -> Optional[
        Union[TraceDataset, PreTrainDataset]]:
        """
        Creates dataset set if not None, otherwise None is returned.
        :param dataset_creator: The optional dataset creator to use.
        :return: None or Dataset
        """
        return dataset_creator.create() if dataset_creator else None

    @staticmethod
    def __assert_index(index_value):
        """
        Asserts that value is instance of DatasetRole
        :param index_value: The value expected to be dataset role.
        :return: None
        """
        if not isinstance(index_value, DatasetRole):
            raise Exception("Expected index to be data role:" + index_value)

    def __getitem__(self, dataset_role: DatasetRole) -> Optional[DATASET_TYPE]:
        """
        Returns the data corresponding to role.
        :param dataset_role: The role of the data returned.
        :return: PreTrainDataset if pretrain role otherwise TraceDataset
        """
        self.__assert_index(dataset_role)
        return self.__datasets[dataset_role]

    def __setitem__(self, dataset_role: DatasetRole, dataset: DATASET_TYPE):
        """
        Sets given data for given attribute corresponding to role
        :param dataset_role: The role defining attribute to set
        :param dataset: The data to set
        :return: None
        """
        self.__assert_index(dataset_role)
        self.__datasets[dataset_role] = dataset

    def __contains__(self, dataset_role: DatasetRole):
        """
        Returns whether data exist for given role.
        :param dataset_role: The role to check a data for.
        :return: Boolean representing whether data exist for role
        """
        return self[dataset_role] is not None

    def __repr__(self):
        """
        Returns string representation of role to type of mapped dataset.
        :return: String representation of trainer data container.
        """
        return str({role.name: type(self[role]) for role in DatasetRole})
