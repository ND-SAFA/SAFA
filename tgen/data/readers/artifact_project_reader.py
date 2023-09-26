import os

from tgen.common.constants.dataset_constants import ARTIFACT_FILE_NAME
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.override import overrides
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
import pandas as pd
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer


class ArtifactProjectReader(AbstractProjectReader[ArtifactDataFrame]):
    """
    Responsible for reading artifacts and trace links and constructing
    a trace dataset.
    """

    def __init__(self, project_path: str, conversions=None, overrides: dict = None):
        """
        Creates reader for project at path and column definitions given.
        :param project_path: Path to the project.
        :param conversions: Column definitions available to project.
        """
        super().__init__(overrides, project_path)
        self.structured_project_reader = StructuredProjectReader(project_path, conversions)

    def read_project(self) -> ArtifactDataFrame:
        """
        Reads project data from files.
        :return: Returns the data frames containing the project artifacts.
        """
        if self.structured_project_reader.get_definition_reader(raise_exception=False) is not None:
            self.structured_project_reader.get_project_definition()
            artifact_df = self.structured_project_reader.read_artifact_df()
        else:
            if not self.get_project_path().endswith(FileUtil.CSV_EXT):
                self.project_path = os.path.join(self.get_project_path(), ARTIFACT_FILE_NAME)
            artifact_df = ArtifactDataFrame(pd.read_csv(self.project_path))
        filtered_artifacts = [artifact_id for artifact_id in artifact_df.index if artifact_id not in artifact_df.index]
        if len(filtered_artifacts) >= 1:
            logger.warning(f"The following artifacts did not contain any content so they have been removed: {filtered_artifacts}")
        return artifact_df

    @overrides(AbstractProjectReader)
    def set_summarizer(self, summarizer: ArtifactsSummarizer) -> None:
        """
        Sets the summarizer used to summarize content read by the reader
        :param summarizer: The summarizer to use
        :return: None
        """
        self.structured_project_reader.set_summarizer(summarizer)

    def get_project_name(self) -> str:
        """
        Gets the name of the project being read.
        :return:  Returns the name of the project being read.
        """
        return self.structured_project_reader.get_project_name()
