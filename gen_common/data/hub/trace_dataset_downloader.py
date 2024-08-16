import os

from datasets import DownloadConfig, DownloadManager

from gen_common.constants import CACHE_DIR_NAME, DATA_PATH
from gen_common.data.hub.abstract_hub_id import AbstractHubId
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util import FileUtil


class TraceDatasetDownloader:
    """
    Responsible for downloading and loading files for supported dataset.
    """

    def __init__(self, descriptor: AbstractHubId, **config_kwargs):
        """
        Initializes adapter for dataset specified in descriptor and converts it to a trace dataset.
        :param descriptor: The name of the dataset to download and prepare.
        :param creator_arguments: Kwargs passed to dataset creator.
        :param config_kwargs: Additional parameters to builder configuration.
        """
        self.descriptor: AbstractHubId = descriptor
        super().__init__(**config_kwargs)  # calls _info where above is needed
        self.trace_dataset_creator = None
        self.data_dir = None
        self.config = DownloadConfig(cache_dir=TraceDatasetDownloader.get_hub_cache_path())
        self.download_manager = DownloadManager(download_config=self.config)

    def download(self) -> str:
        """
        Downloads or reads cache for dataset.
        TODO: Check to see if works with multiple datasets using same url
        :return: Returns path to dataset.
        """
        if self.data_dir is None:
            data_path = self.descriptor.get_path()
            if os.path.exists(data_path):
                data_dir = data_path
                logger.info(f"Loading local path: {data_path}")
            else:
                data_dir = self.download_or_load(data_path)
            assert os.path.isdir(data_dir), f"Expected {data_dir} to be folder."
            self.data_dir = data_dir
        return self.data_dir

    def download_or_load(self, data_path):
        """
        Downloads url or loads it from cache.
        :param data_path: URL path to dataset.
        :return: Local path to downloaded dataset.
        """
        logger.info(f"Downloading dataset from hub: {data_path}")
        download_path = self.download_manager.download_and_extract(data_path)
        zip_file_query = FileUtil.ls_dir(download_path, ignore=["__MACOSX"])
        assert len(zip_file_query) == 1, f"Found more than one folder for extracted files:{zip_file_query}"
        data_dir = zip_file_query[0]  # include path to directory
        return data_dir

    @staticmethod
    def get_hub_cache_path() -> str:
        """
        :return:Returns path hub path cache directory.
        """
        hub_path = os.path.join(DATA_PATH, CACHE_DIR_NAME)
        hub_path = os.path.expanduser(hub_path)
        return hub_path
