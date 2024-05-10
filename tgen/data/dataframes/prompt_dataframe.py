from typing import Type

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.prompt_keys import PromptKeys


class PromptDataFrame(AbstractProjectDataFrame):
    """
    Contains the layers that are linked found in a project
    """

    OPTIONAL_COLUMNS = [PromptKeys.COMPLETION.value,
                        PromptKeys.PROMPT_BUILDER_ID.value,
                        PromptKeys.SYSTEM.value]

    @classmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """
        return None

    @classmethod
    def data_keys(cls) -> Type:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """
        return PromptKeys

    def add_prompt(self, prompt: str, completion: str = EMPTY_STRING, prompt_builder_id: str = None) -> EnumDict:
        """
        Adds prompt and completion pair to dataframe
        :param prompt: The prompt
        :param completion: The completion/response
        :param prompt_builder_id: The id of the prompt builder the prompt was constructed from
        :return: The prompt and completion pair
        """
        return self.add_row({PromptKeys.PROMPT: prompt,
                             PromptKeys.COMPLETION: completion,
                             PromptKeys.PROMPT_BUILDER_ID: prompt_builder_id})
