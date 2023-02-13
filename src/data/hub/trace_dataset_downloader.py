import os

from datasets import DownloadConfig, DownloadManager

from constants import CACHE_DIR_NAME, DATA_PATH_PARAM
from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor
from data.hub.supported_datasets import SupportedDatasets
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from util.file_util import FileUtil
from util.json_util import JsonUtil


class TraceDatasetDownloader:
    """
    Responsible for downloading and loading files for supported dataset.
    """

    def __init__(self, dataset_name: str, **config_kwargs):
        """
        Initializes adapter for dataset specified in descriptor and converts it to a trace dataset.
        :param dataset_name: The name of the dataset to download and prepare.
        :param creator_arguments: Kwargs passed to dataset creator.
        :param config_kwargs: Additional parameters to builder configuration.
        """
        self.dataset_name = dataset_name
        self.descriptor: AbstractDatasetDescriptor = SupportedDatasets.get_value(dataset_name)
        super().__init__(**config_kwargs)  # calls _info where above is needed
        self.trace_dataset_creator = None
        self.project_path = None

    def download(self) -> str:
        """
        Downloads or reads cache for dataset.
        :return: Returns path to dataset.
        """
        if self.project_path is None:
            hub_path = os.path.join(os.environ[DATA_PATH_PARAM], CACHE_DIR_NAME)
            hub_path = os.path.expanduser(hub_path)
            download_config = DownloadConfig(cache_dir=hub_path)
            download_manager = DownloadManager(download_config=download_config)
            data_dir = download_manager.download_and_extract(self.descriptor.get_url())
            assert os.path.isdir(data_dir), f"Expected {data_dir} to be folder."
            zip_file_query = FileUtil.ls_dir(data_dir)
            assert len(zip_file_query) == 1, f"Found more than one folder for extracted files:{zip_file_query}"
            self.project_path = zip_file_query[0]  # include path to directory
            definition_content = JsonUtil.dict_to_json(self.descriptor.get_definition())
            definition_file_path = os.path.join(self.project_path, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)
            FileUtil.write(definition_content, definition_file_path)
        return self.project_path
