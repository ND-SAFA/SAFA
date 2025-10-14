import os
from typing import Dict, Tuple

from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.data.processing.augmentation.data_augmenter import DataAugmenter
from gen_common.data.readers.csv_project_reader import CsvProjectReader
from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.data.tdatasets.idataset import iDataset


class DeterministicTrainerDatasetManager(TrainerDatasetManager):
    DETERMINISTIC_KEY = "deterministic_id"

    def __init__(self,
                 pre_train_dataset_creator: MLMPreTrainDatasetCreator = None,
                 train_dataset_creator: AbstractDatasetCreator = None,
                 val_dataset_creator: AbstractDatasetCreator = None,
                 eval_dataset_creator: AbstractDatasetCreator = None,
                 augmenter: DataAugmenter = None,
                 output_dir: str = None,
                 random_seed: int = None
                 ):
        """
        Container to hold all the data used in the TraceTrainer
        :param pre_train_dataset_creator: The pre-training dataset creator.
        :param train_dataset_creator: The training dataset creator.
        :param val_dataset_creator: the validation dataset creator.
        :param eval_dataset_creator: The training dataset creator.data
        :param augmenter: augmenter to use for augmenting datasets
        :param output_dir: where to save the datasets to
        :param random_seed: the random seed for this split
        """
        super().__init__(pre_train_dataset_creator, train_dataset_creator, val_dataset_creator, eval_dataset_creator,
                         augmenter=augmenter)
        self.output_dir = output_dir
        self.dataset_name = self.get_creator(DatasetRole.TRAIN).get_name() if self.get_creator(DatasetRole.TRAIN) is not None \
            else "Unknown_Dataset"
        self.random_seed = random_seed

    def get_datasets(self) -> Dict[DatasetRole, iDataset]:
        """
        Gets the dictionary mapping dataset role to the dataset
        :return: the dictionary of datasets
        """
        if not self._datasets:
            self._datasets, reloaded = self._create_datasets_from_creators_deterministic(self._dataset_creators)
            if DatasetRole.TRAIN in self._datasets:
                self._datasets[DatasetRole.TRAIN] = self._prepare_datasets(self._datasets[DatasetRole.TRAIN], self.augmenter)
            if not reloaded:
                self.export_dataset_splits(self.get_output_path(), SupportedDatasetExporter.CSV)
        return self._datasets

    def get_output_path(self) -> str:
        """
        Gets the path where datasets should be saved
        :return: the output path
        """
        output_path = os.path.join(self.output_dir, self.dataset_name) if self.output_dir else self.dataset_name
        if self.random_seed:
            output_path = os.path.join(output_path, str(self.random_seed))
        return output_path

    def _create_datasets_from_creators_deterministic(self, dataset_creators_map: Dict[DatasetRole, AbstractDatasetCreator]) \
            -> Tuple[Dict[DatasetRole, TrainerDatasetManager.DATASET_TYPE], bool]:
        """
        Creates the data from their corresponding creators so that splits are deterministic
        :param dataset_creators_map: Map of role to dataset creator to make deterministic.
        :return: a dictionary mapping dataset role to the corresponding dataset and a bool which is True if the datasets are reloaded
        """
        deterministic_dataset_creators_map = {}
        reloaded = False
        for dataset_role in dataset_creators_map.keys():
            dataset_filepath = os.path.join(self.get_output_path(), self.get_dataset_filename(dataset_role,
                                                                                              dataset_name=self.dataset_name))
            if os.path.exists(dataset_filepath):
                deterministic_dataset_creators_map[dataset_role] = TraceDatasetCreator(CsvProjectReader(dataset_filepath),
                                                                                       allowed_orphans=5)
                reloaded = True
            else:
                deterministic_dataset_creators_map[dataset_role] = dataset_creators_map[dataset_role]
        self._dataset_creators = deterministic_dataset_creators_map
        return super()._create_datasets_from_creators(deterministic_dataset_creators_map), reloaded
