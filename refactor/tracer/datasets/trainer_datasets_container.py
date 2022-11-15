from typing import Dict, List, Optional, Tuple

from config.constants import RESAMPLE_RATE_DEFAULT, VALIDATION_PERCENTAGE_DEFAULT
from tracer.datasets.abstract_dataset import AbstractDataset
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.datasets.dataset_role import DatasetRole
from tracer.datasets.pre_train_dataset import PreTrainDataset
from tracer.datasets.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processing_option import PreProcessingOption


class TrainerDatasetsContainer:

    def __init__(self, datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]],
                 dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]] = None,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT, split_train_dataset: bool = False,
                 resample_rate: int = RESAMPLE_RATE_DEFAULT
                 ):
        """
        Container to hold all the datasets used in the TraceTrainer
        :param datasets_map: dictionary mapping datasets role (e.g. train/eval) to the desired datasets creator and its params
        :param dataset_pre_processing_options: dictionary mapping datasets role to the desired pre-processing steps and related params
        :param validation_percentage: percentage of the data to use for validation datasets
        :param split_train_dataset: if True, splits the training datasets into a train, val datasets
        :param resample_rate: the rate at which to resample positive examples in the train datasets
        """
        self.pre_train_dataset: Optional[PreTrainDataset] = None
        self.train_dataset: Optional[AbstractDataset] = None
        self.val_dataset: Optional[AbstractDataset] = None
        self.eval_dataset: Optional[TraceDataset] = None
        self.dataset_pre_processing_options = dataset_pre_processing_options

        self._make_datasets(datasets_map, dataset_pre_processing_options if dataset_pre_processing_options else {},
                            validation_percentage, split_train_dataset, resample_rate)

    def _make_datasets(self, datasets_map: Dict[DatasetRole, Tuple[SupportedDatasetCreator, Dict]],
                       dataset_pre_processing_options: Dict[DatasetRole, Tuple[List[PreProcessingOption], Dict]],
                       validation_percentage: float, split_train_dataset: bool, resample_rate: int) -> None:
        """
        Handles making the datasets for each datasets role
        :param datasets_map:
        :param dataset_pre_processing_options:
        :param validation_percentage:
        :param split_train_dataset:
        :param resample_rate:
        :return:
        """
        for dataset_role, dataset_creator_reqs in datasets_map.items():
            dataset_creator_class, dataset_creator_params = dataset_creator_reqs
            self[dataset_role] = self._make_dataset(dataset_creator_class, dataset_creator_params,
                                                    dataset_pre_processing_options.get(dataset_role, None))
        if isinstance(self.train_dataset, TraceDataset) and split_train_dataset:
            self.train_dataset, self.val_dataset = self.train_dataset.train_test_split(validation_percentage,
                                                                                       resample_rate)

    @staticmethod
    def _make_dataset(dataset_creator_class: SupportedDatasetCreator, dataset_creator_params: Dict,
                      pre_processing_params: Tuple[List[PreProcessingOption], Dict]) -> Optional[AbstractDataset]:
        """
        Handles making the datasets for a specified role and the given parameters
        :param dataset_creator_class: the class to use to create datasets
        :param dataset_creator_params: dictionary of parameters for the datasets creator to use when creating datasets
        :param pre_processing_params: tuple containing the desired pre-processing steps and related params
        :return: the datasets
        """
        dataset_creator = dataset_creator_class.value(pre_processing_params=pre_processing_params,
                                                      **dataset_creator_params)
        return dataset_creator.create()

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
