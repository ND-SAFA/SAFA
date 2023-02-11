import os

from datasets import DownloadConfig, DownloadManager

from data.hub.abstract_dataset_descriptor import AbstractDatasetDescriptor
from data.hub.supported_datasets import SupportedDatasets
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from util.file_util import FileUtil
from util.json_util import JsonUtil


class TraceDatasetDownloader:
    """
    Experimental dataset for software traceability.
    Refer https://huggingface.co/docs/datasets/add_dataset.html for more information
    Load data in stream: https://huggingface.co/docs/datasets/dataset_streaming.html
    """

    def __init__(self, dataset_name: str, zip_file_name: str = None, **config_kwargs):
        """
        Initializes adapter for dataset specified in descriptor and converts it to a trace dataset.
        :param dataset_name: The name of the dataset to download and prepare.
        :param creator_arguments: Kwargs passed to dataset creator.
        :param config_kwargs: Additional parameters to builder configuration.
        """
        if zip_file_name is None:
            zip_file_name = dataset_name
        self.dataset_name = dataset_name
        self.zip_file_name = zip_file_name
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
            hub_path = os.path.join(os.environ["DATA_PATH"], "HuggingFace")
            hub_path = os.path.expanduser(hub_path)
            download_config = DownloadConfig(cache_dir=hub_path)
            download_manager = DownloadManager(download_config=download_config)
            data_dir = download_manager.download_and_extract(self.descriptor.get_url())
            assert os.path.isdir(data_dir), f"Expected {data_dir} to be folder."
            definition_content = JsonUtil.dict_to_json(self.descriptor.get_definition())
            self.project_path = os.path.join(data_dir, self.zip_file_name)
            definition_file_path = os.path.join(self.project_path, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)
            FileUtil.write(definition_content, definition_file_path)
        return self.project_path
