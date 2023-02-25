import os

from datasets import DownloadConfig, DownloadManager

from constants import CACHE_DIR_NAME, DATA_PATH_PARAM
from data.hub.abstract_hub_id import AbstractHubId
from util.file_util import FileUtil
from util.json_util import JsonUtil


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

    def download(self) -> str:
        """
        Downloads or reads cache for dataset.
        TODO: Check to see if works with multiple datasets using same url
        :return: Returns path to dataset.
        """
        if self.data_dir is None:
            hub_path = os.path.join(os.environ[DATA_PATH_PARAM], CACHE_DIR_NAME)
            hub_path = os.path.expanduser(hub_path)
            download_config = DownloadConfig(cache_dir=hub_path)
            download_manager = DownloadManager(download_config=download_config)
            data_dir = download_manager.download_and_extract(self.descriptor.get_url())
            assert os.path.isdir(data_dir), f"Expected {data_dir} to be folder."
            definition_content = JsonUtil.dict_to_json(self.descriptor.get_definition())
            definition_file_path = self.descriptor.get_definition_path(data_dir)
            FileUtil.write(definition_content, definition_file_path)
            self.data_dir = data_dir
        return self.data_dir
