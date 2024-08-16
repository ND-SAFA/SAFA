from gen_common.data.dataframes.prompt_dataframe import PromptDataFrame
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.util import FileUtil
from gen_common.util.json_util import JsonUtil


class PromptProjectReader(AbstractProjectReader[PromptDataFrame]):
    """
    Responsible for reading prompt dataframes containing prompt, completion for LLMs
    """

    FILE_EXT = ".jsonl"

    def __init__(self, project_path: str):
        """
        Creates reader for project at path and column definitions given.
        :param project_path: Path to the project.
        """
        super().__init__(project_path=project_path)
        assert FileUtil.get_file_ext(project_path) == self.FILE_EXT, f"Expected project path to be a {self.FILE_EXT} file"

    def read_project(self) -> PromptDataFrame:
        """
        Reads project data from files.
        :return: Returns the data frames containing the project artifacts.
        """
        prompt_df = PromptDataFrame(JsonUtil.read_jsonl_file(self.get_full_project_path()))
        if self.summarizer is not None:
            prompt_df[PromptKeys.PROMPT.value] = self.summarizer.summarize_dataframe(prompt_df, PromptKeys.PROMPT.value)
        return prompt_df

    def get_project_name(self) -> str:
        """
        Gets the name of the project being read.
        :return:  Returns the name of the project being read.
        """
        return FileUtil.get_file_name(self.get_full_project_path())
