import os
from collections import OrderedDict
from typing import Dict, List, Optional, Union

import pandas as pd
from datasets import disable_caching

from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.enum_util import EnumDict, EnumUtil
from common_resources.tools.util.override import overrides
from common_resources.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from common_resources.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from common_resources.data.creators.split_dataset_creator import SplitDatasetCreator
from common_resources.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from common_resources.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from common_resources.data.keys.csv_keys import CSVKeys
from common_resources.data.processing.augmentation.data_augmenter import DataAugmenter
from common_resources.data.splitting.dataset_splitter import DatasetSplitter
from common_resources.data.splitting.supported_split_strategy import SupportedSplitStrategy
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.data.tdatasets.pre_train_dataset import PreTrainDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.model_manager import ModelManager
from common_resources.tools.variables.undetermined_variable import UndeterminedVariable

disable_caching()


class TrainerDatasetManager(BaseObject):
    DATASET_TYPE = Union[TraceDataset, PreTrainDataset, iDataset]

    def __init__(self,
                 pre_train_dataset_creator: MLMPreTrainDatasetCreator = None,
                 train_dataset_creator: AbstractDatasetCreator = None,
                 val_dataset_creator: AbstractDatasetCreator = None,
                 eval_dataset_creator: AbstractDatasetCreator = None,
                 augmenter: DataAugmenter = None):
        """
        Container to hold all the data used in the TraceTrainer
        :param pre_train_dataset_creator: The pre-training dataset creator.
        :param train_dataset_creator: The training dataset creator.
        :param val_dataset_creator: the validation dataset creator.
        :param eval_dataset_creator: The training dataset creator.data
        :param augmenter: augmenter to use for augmenting datasets
        """

        self._dataset_creators = {DatasetRole.PRE_TRAIN: pre_train_dataset_creator,
                                  DatasetRole.TRAIN: train_dataset_creator,
                                  DatasetRole.VAL: val_dataset_creator,
                                  DatasetRole.EVAL: eval_dataset_creator}
        self._datasets = {}
        self._hf_datasets = None
        self.augmenter = augmenter

    def get_creator(self, dataset_role: DatasetRole) -> AbstractDatasetCreator:
        """
        Gets the dataset creator for the given role
        :param dataset_role: the dataset role
        :return: the dataset creator for the given role
        """
        return self._dataset_creators.get(dataset_role, None)

    def export_dataset_splits(self, output_dir: str, format_type: SupportedDatasetExporter = SupportedDatasetExporter.CSV) \
            -> List[str]:
        """
        Saves all dataset splits to the output dir
        :param output_dir: directory to save to
        :param format_type: The type of format to save dataset splits.
        :return: the list of files that were saved
        """
        output_paths = []
        datasets = self.get_datasets() if not self._datasets else self._datasets
        for dataset_role in DatasetRole:
            if dataset_role in datasets and datasets[dataset_role] is not None:
                dataset = datasets[dataset_role]
                exporter: AbstractDatasetExporter = format_type.value
                export_path = os.path.join(output_dir, self.get_dataset_filename(dataset_role)) \
                    if exporter.include_filename() else os.path.join(output_dir, dataset_role.value)
                output_path = exporter(export_path=export_path, dataset=dataset).export()
                output_paths.append(output_path)
        return output_paths

    @staticmethod
    def create_from_map(dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) -> "TrainerDatasetManager":
        """
        Creates instance containing dataset for each mapped role.
        :param dataset_creators_map: The map of roles to data to set in instance.
        :return: TrainerDatasetManager with initialized data.
        """
        return TrainerDatasetManager(
            pre_train_dataset_creator=dataset_creators_map.get(DatasetRole.PRE_TRAIN, None),
            train_dataset_creator=dataset_creators_map.get(DatasetRole.TRAIN, None),
            val_dataset_creator=dataset_creators_map.get(DatasetRole.VAL, None),
            eval_dataset_creator=dataset_creators_map.get(DatasetRole.EVAL, None))

    @staticmethod
    def create_from_datasets(dataset_map: Dict[DatasetRole, Union[iDataset, List[iDataset]]] = None,
                             **datasets_as_kwargs) -> "TrainerDatasetManager":
        """
        Creates instance containing dataset for each mapped role.
        :param dataset_map: The map of roles to data to set in instance.
        :return: TrainerDatasetManager with initialized data.
        """
        dataset_map = EnumDict(datasets_as_kwargs) if not dataset_map else dataset_map
        trainer_dataset_manager = TrainerDatasetManager()
        for role in DatasetRole:
            if role not in dataset_map:
                trainer_dataset_manager._datasets[role] = None
            else:
                dataset = dataset_map[role]
                datasets = dataset if isinstance(dataset, list) else [dataset]
                for d in datasets:
                    assert isinstance(d, iDataset), f"Unexpected type of dataset {type(d)}"
                trainer_dataset_manager._datasets[role] = dataset
        return trainer_dataset_manager

    @overrides(BaseObject)
    def use_values_from_object_for_undetermined(self, obj: "TrainerDatasetManager") -> None:
        """
        Fills in any undetermined values in self by using values from the given object
        :param obj: the object to use to fill in values
        :return: None
        """
        for dataset_role, dataset_creator in self._dataset_creators.items():
            creator = obj.get_creator(dataset_role)
            if creator is None:
                continue
            if isinstance(dataset_creator, UndeterminedVariable):
                self._dataset_creators[dataset_role] = creator
            elif isinstance(dataset_creator, BaseObject):
                self._dataset_creators[dataset_role].use_values_from_object_for_undetermined(creator)
        super().use_values_from_object_for_undetermined(obj)

    def get_datasets(self) -> Dict[DatasetRole, iDataset]:
        """
        Gets the dictionary mapping dataset role to the dataset
        :return: the dictionary of datasets
        """
        if not self._datasets:
            self._datasets = self._create_datasets_from_creators(self._dataset_creators)
            if DatasetRole.TRAIN in self._datasets:
                self._datasets[DatasetRole.TRAIN] = self._prepare_datasets(self._datasets[DatasetRole.TRAIN], self.augmenter)
        return self._datasets

    def replace_dataset(self, new_dataset: iDataset, dataset_role: DatasetRole) -> None:
        """
        Replaces the dataset for the given dataset role with the new dataset
        :param new_dataset: The dataset to replace the original dataset with
        :param dataset_role: The role of the dataset being replaced
        :return: None
        """
        datasets = self.get_datasets()
        datasets[dataset_role] = new_dataset

    def get_hf_datasets(self, model_manager: ModelManager) -> Dict[str, pd.DataFrame]:
        """
        Gets all datasets in the expected hugging face format
        :param model_manager: The model manager to use for tokenization
        :return: A dictionary mapping all dataset roles to their expected hugging face format
        """
        if self._hf_datasets is None:
            self._hf_datasets = {}
            datasets = self.get_datasets()
            for role, dataset in datasets.items():
                if dataset is None:
                    continue
                self._hf_datasets[role] = dataset.to_hf_dataset(model_manager)
        return self._hf_datasets

    def cleanup(self) -> None:
        """
        Clears datasets out of memory
        :return: None
        """
        self._datasets = None

    def get_dataset_filename(self, dataset_role: DatasetRole, dataset_name: str = None) -> str:
        """
        Returns the filename associated with the dataset corresponding to the given role
        :param dataset_role: the role of the dataset.
        :param dataset_name: The name of the dataset to override.
        :return: the dataset filename
        """
        if not dataset_name:
            dataset_name = self.get_creator(dataset_role).get_name() if self.get_creator(dataset_role) is not None \
                else type(self.get_datasets()[dataset_role])
        return f"{dataset_name}_{dataset_role.name.lower()}{CSVKeys.EXT}"

    def _prepare_datasets(self, train_dataset: iDataset, data_augmenter: DataAugmenter) -> iDataset:
        """
        Performs any necessary additional steps necessary to prepare each dataset
        :param train_dataset: The dataset used to calculate the splits off of.
        :param data_augmenter: The augmenter responsible for generating new positive samples.
        :return: None
        """
        if train_dataset:
            dataset_splits_map = self._create_dataset_splits(train_dataset, self._dataset_creators)
            self._datasets.update(dataset_splits_map)
            if DatasetRole.TRAIN in dataset_splits_map:
                train_dataset = dataset_splits_map[DatasetRole.TRAIN]
                if isinstance(train_dataset, TraceDataset):
                    train_dataset.prepare_for_training(data_augmenter)
        return train_dataset

    @staticmethod
    def _create_dataset_splits(train_dataset: TraceDataset,
                               dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) -> Dict[DatasetRole, iDataset]:
        """
        Splits the train dataset into desired splits and creates a dictionary mapping dataset role to split for all split data
        :param train_dataset: the train dataset
        :param dataset_creators_map: a map of dataset role to all dataset creators
        :return: a dictionary mapping dataset role to split for all split data
        """
        dataset_role_to_split_percentage: OrderedDict[DatasetRole, float] = OrderedDict()
        strategies: List[SupportedSplitStrategy] = []
        for dataset_role, dataset_creator in dataset_creators_map.items():
            if isinstance(dataset_creator, SplitDatasetCreator):
                dataset_creator.name = dataset_creators_map[DatasetRole.TRAIN].get_name()
                split_strategy_enum = EnumUtil.get_enum_from_name(SupportedSplitStrategy, dataset_creator.split_strategy) \
                    if not isinstance(dataset_creator.split_strategy, SupportedSplitStrategy) else dataset_creator.split_strategy
                strategies.append(split_strategy_enum)
                dataset_role_to_split_percentage[dataset_role] = dataset_creator.val_percentage
        if len(dataset_role_to_split_percentage) < 1:
            return {}
        dataset_role_to_split_percentage[DatasetRole.TRAIN] = 1 - sum(dataset_role_to_split_percentage.values())
        dataset_role_to_split_percentage.move_to_end(DatasetRole.TRAIN, last=False)
        splitter = DatasetSplitter(train_dataset, dataset_role_to_split_percentage, strategies)
        return splitter.split_dataset()

    @staticmethod
    def _create_datasets_from_creators(dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) \
            -> Dict[DatasetRole, DATASET_TYPE]:
        """
        Creates the data from their corresponding creators
        :param dataset_creators_map: Map of dataset role to dataset creator.
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
            raise Exception(f"Expected index to be data role but got {index_value}")

    def get_split_size(self, dataset_role: DatasetRole) -> Optional[float]:
        """
        Returns the size of the split at the given dataset role.
        :param dataset_role: The role of the split size to return.
        :return: The split size if role is split dataset creator else None.
        """
        for role, creator in self._dataset_creators.items():
            if role != dataset_role:
                continue
            if isinstance(creator, SplitDatasetCreator):
                return creator.val_percentage
        return None

    def __getitem__(self, dataset_role: DatasetRole) -> Optional[DATASET_TYPE]:
        """
        Returns the data corresponding to role.
        :param dataset_role: The role of the data returned.
        :return: PreTrainDataset if pretrain role otherwise TraceDataset
        """
        self.__assert_index(dataset_role)
        return self.get_datasets()[dataset_role]

    def __setitem__(self, dataset_role: DatasetRole, dataset: DATASET_TYPE):
        """
        Sets given data for given attribute corresponding to role
        :param dataset_role: The role defining attribute to set
        :param dataset: The data to set
        :return: None
        """
        self.__assert_index(dataset_role)
        self.get_datasets()[dataset_role] = dataset

    def __contains__(self, dataset_role: DatasetRole):
        """
        Returns whether data exist for given role.
        :param dataset_role: The role to check a data for.
        :return: Boolean representing whether data exist for role
        """
        return self._dataset_creators.get(dataset_role, None) is not None or self._datasets.get(dataset_role, None) is not None

    def __repr__(self) -> str:
        """
        Returns string representation of role to type of mapped dataset.
        :return: String representation of trainer data container.
        """
        return str({role.name: type(self.get_creator(role)) for role in DatasetRole}) if self._dataset_creators is not None \
            else str({role.name: type(self.get_datasets()[role]) for role in DatasetRole})
