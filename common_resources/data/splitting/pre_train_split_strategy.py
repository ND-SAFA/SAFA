import os
from typing import Tuple

from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.override import overrides
from common_resources.data.readers.pre_train_project_reader import PreTrainProjectReader
from common_resources.data.splitting.abstract_split_strategy import AbstractSplitStrategy
from common_resources.data.tdatasets.pre_train_dataset import PreTrainDataset


class PreTrainSplitStrategy(AbstractSplitStrategy):
    """
    Representing a strategy for splitting a pretraining dataset.
    """

    SPLIT_DIR_NAME = "split_{}"

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(dataset: PreTrainDataset, second_split_percentage: float) -> Tuple[PreTrainDataset, PreTrainDataset]:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :param second_split_percentage: The percentage of the data to be contained in second split
        :return: Dataset containing slice of data.
        """
        file_contents = FileUtil.read_file(dataset.training_file_path).split(PreTrainProjectReader.DELIMINATOR)
        content1, content2 = AbstractSplitStrategy.split_data(file_contents, second_split_percentage)
        base_dir, filename = FileUtil.split_base_path_and_filename(dataset.training_file_path)
        splits = []
        for i, content in enumerate([content1, content2]):
            split_path = PreTrainSplitStrategy.make_split_training_path(base_dir, i, filename)
            FileUtil.write(PreTrainProjectReader.DELIMINATOR.join(content), split_path)
            splits.append(PreTrainDataset(training_file_path=split_path, block_size=dataset.block_size, **dataset.kwargs))
        return splits[0], splits[1]

    @staticmethod
    def make_split_training_path(base_dir: str, split_num: int, filename: str) -> str:
        """
        Constructs the training path for the new split
        :param base_dir: The base path to the directory to save splits
        :param split_num: The number corresponding with this split
        :param filename: The name of the file to save the data in
        :return: The training path for the split
        """
        return os.path.join(base_dir, PreTrainSplitStrategy.SPLIT_DIR_NAME.format(split_num), filename)
