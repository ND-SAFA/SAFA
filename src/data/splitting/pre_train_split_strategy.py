import os

from data.datasets.pre_train_dataset import PreTrainDataset
from data.readers.pre_train_project_reader import PreTrainProjectReader
from data.splitting.abstract_split_strategy import AbstractSplitStrategy
from util.file_util import FileUtil


class PreTrainSplitStrategy(AbstractSplitStrategy):
    """
    Representing a strategy for splitting a pretraining dataset.
    """

    SPLIT_DIR_NAME = "split_{}"

    @staticmethod
    def create_split(dataset: PreTrainDataset, percent_split: float, slice_num: int) -> PreTrainDataset:
        """
        Creates the split of the pretraining dataset
        :param dataset: The dataset to split.
        :type percent_split: The percentage of the dataset contained in the second split.
        :type slice_num: The slice number to return.
        :return: PreTrainDataset containing slice of data.
        """
        file_contents = FileUtil.read_file(dataset.training_file_path).split(PreTrainProjectReader.DELIMINATOR)
        split_contents = AbstractSplitStrategy.split_data(file_contents, percent_split)[slice_num - 1]
        base_dir, filename = FileUtil.split_base_path_and_filename(dataset.training_file_path)
        new_training_path = os.path.join(base_dir, PreTrainSplitStrategy.SPLIT_DIR_NAME.format(slice_num), filename)
        FileUtil.write(PreTrainProjectReader.DELIMINATOR.join(split_contents), new_training_path)
        return PreTrainDataset(training_file_path=new_training_path, block_size=dataset.block_size, **dataset.kwargs)
