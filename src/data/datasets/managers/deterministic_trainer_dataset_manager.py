import os
from typing import Dict, Tuple

from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.creators.csv_dataset_creator import CSVDatasetCreator
from data.datasets.dataset_role import DatasetRole
from data.datasets.keys.csv_format import CSVKeys
from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from data.processing.augmentation.data_augmenter import DataAugmenter


class DeterministicTrainerDatasetManager(TrainerDatasetManager):
    DETERMINISTIC_KEY = "deterministic_output_dir"

    def __init__(self,
                 deterministic_output_dir: str,
                 pre_train_dataset_creator: AbstractDatasetCreator = None,
                 train_dataset_creator: AbstractDatasetCreator = None,
                 val_dataset_creator: AbstractDatasetCreator = None,
                 eval_dataset_creator: AbstractDatasetCreator = None,
                 augmenter: DataAugmenter = None,
                 ):
        """
        Container to hold all the data used in the TraceTrainer
        :param deterministic_output_dir: where datasets will be saved + loaded
        :param pre_train_dataset_creator: The pre-training dataset creator.
        :param train_dataset_creator: The training dataset creator.
        :param val_dataset_creator: the validation dataset creator.
        :param eval_dataset_creator: The training dataset creator.data
        :param augmenter: augmenter to use for augmenting datasets
        """
        super().__init__(pre_train_dataset_creator, train_dataset_creator, val_dataset_creator, eval_dataset_creator, augmenter)
        self.output_dir = deterministic_output_dir

    def get_datasets(self) -> Dict[DatasetRole, AbstractDataset]:
        """
        Gets the dictionary mapping dataset role to the dataset
        :return: the dictionary of datasets
        """
        if self._datasets is None:
            self._datasets, reloaded = self._create_datasets_from_creators_deterministic(self._dataset_creators)
            if not reloaded:
                self._prepare_datasets(self.augmenter)
                self.save_dataset_splits(self.output_dir)
        return self._datasets

    def _create_datasets_from_creators_deterministic(self, dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) \
            -> Tuple[Dict[DatasetRole, TrainerDatasetManager.DATASET_TYPE], bool]:
        """
        Creates the data from their corresponding creators so that splits are deterministic
        :return: a dictionary mapping dataset role to the corresponding dataset and a bool which is True if the datasets are reloaded
        """
        deterministic_dataset_creators_map = {}
        reloaded = False
        for dataset_role in dataset_creators_map.keys():
            dataset_filepath = os.path.join(self.output_dir, self._get_dataset_filename(dataset_role)) + CSVKeys.EXT
            if os.path.exists(dataset_filepath):
                deterministic_dataset_creators_map[dataset_role] = CSVDatasetCreator(data_file_path=dataset_filepath)
                reloaded = True
            else:
                deterministic_dataset_creators_map[dataset_role] = dataset_creators_map[dataset_role]
        return super()._create_datasets_from_creators(deterministic_dataset_creators_map), reloaded
