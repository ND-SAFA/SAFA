import os
from typing import Dict, Tuple

from data.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.dataset_role import DatasetRole
from data.keys.csv_format import CSVKeys
from data.managers.trainer_dataset_manager import TrainerDatasetManager
from data.processing.augmentation.data_augmenter import DataAugmenter
from data.readers.csv_project_reader import CsvProjectReader


class DeterministicTrainerDatasetManager(TrainerDatasetManager):
    DETERMINISTIC_KEY = "deterministic_id"

    def __init__(self,
                 deterministic_id: str,
                 pre_train_dataset_creator: MLMPreTrainDatasetCreator = None,
                 train_dataset_creator: AbstractDatasetCreator = None,
                 val_dataset_creator: AbstractDatasetCreator = None,
                 eval_dataset_creator: AbstractDatasetCreator = None,
                 augmenter: DataAugmenter = None,
                 output_dir: str = None
                 ):
        """
        Container to hold all the data used in the TraceTrainer
        :param deterministic_id: identifier for this set of splits
        :param pre_train_dataset_creator: The pre-training dataset creator.
        :param train_dataset_creator: The training dataset creator.
        :param val_dataset_creator: the validation dataset creator.
        :param eval_dataset_creator: The training dataset creator.data
        :param augmenter: augmenter to use for augmenting datasets
        :param output_dir: where to save the datasets to
        """
        super().__init__(pre_train_dataset_creator, train_dataset_creator, val_dataset_creator, eval_dataset_creator, augmenter)
        self.deterministic_id = deterministic_id
        self.output_dir = output_dir

    def get_datasets(self) -> Dict[DatasetRole, AbstractDataset]:
        """
        Gets the dictionary mapping dataset role to the dataset
        :return: the dictionary of datasets
        """
        if self._datasets is None:
            self._datasets, reloaded = self._create_datasets_from_creators_deterministic(self._dataset_creators)
            if not reloaded:
                self._prepare_datasets(self.augmenter)
                self.save_dataset_splits(self.get_output_path())
        return self._datasets

    def get_output_path(self) -> str:
        """
        Gets the path where datasets should be saved
        :return: the output path
        """
        if self.output_dir:
            return os.path.join(self.output_dir, self.deterministic_id)
        return self.deterministic_id

    def _create_datasets_from_creators_deterministic(self, dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) \
            -> Tuple[Dict[DatasetRole, TrainerDatasetManager.DATASET_TYPE], bool]:
        """
        Creates the data from their corresponding creators so that splits are deterministic
        :return: a dictionary mapping dataset role to the corresponding dataset and a bool which is True if the datasets are reloaded
        """
        deterministic_dataset_creators_map = {}
        reloaded = False
        for dataset_role in dataset_creators_map.keys():
            dataset_filepath = os.path.join(self.get_output_path(), self._get_dataset_filename(dataset_role)) + CSVKeys.EXT
            if os.path.exists(dataset_filepath):
                deterministic_dataset_creators_map[dataset_role] = TraceDatasetCreator(CsvProjectReader(dataset_filepath),
                                                                                       allowed_orphans=5)
                reloaded = True
            else:
                deterministic_dataset_creators_map[dataset_role] = dataset_creators_map[dataset_role]
        return super()._create_datasets_from_creators(deterministic_dataset_creators_map), reloaded
