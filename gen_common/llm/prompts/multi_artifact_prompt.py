from copy import deepcopy
from enum import Enum, auto
from typing import Dict, List

from gen_common.constants import EMPTY_STRING, MAX_TOKENS_FOR_NO_SUMMARIES, NEW_LINE
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.tokens.token_calculator import TokenCalculator
from gen_common.util import DictUtil, EnumDict
from gen_common.util.override import overrides


class MultiArtifactPrompt(Prompt):
    """
    Responsible for formatting and parsing of presenting many artifacts in a prompt
    """

    class BuildMethod(Enum):
        """
        The method to build the prompt (determines prompt format)
        """
        XML = auto()
        NUMBERED = auto()
        MARKDOWN = auto()

    class DataType(Enum):
        TRACES = auto()
        ARTIFACT = auto()

    def __init__(self, prompt_start: str = EMPTY_STRING,
                 build_method: BuildMethod = BuildMethod.NUMBERED,
                 data_type: DataType = DataType.ARTIFACT,
                 starting_num: int = 1,
                 include_ids: bool = True,
                 prompt_args: PromptArgs = None,
                 **artifact_params):
        """
        Constructor for making a prompt containing many artifacts.
        :param prompt_start: The prefix to attach to prompt.
        :param prompt_args: The args to the base prompt.
        :param build_method: The method to build the prompt (determines prompt format).
        :param data_type: Whether the data is coming from artifacts or traces
        :param starting_num: The number to start the artifacts at if using numbered build method
        :param include_ids: Whether to include artifact IDs in prompt.
        :param artifact_params: Parameters used to initialize artifact prompt
        """
        self.build_method = build_method
        self.build_methods = {self.BuildMethod.XML: self._build_as_xml,
                              self.BuildMethod.NUMBERED: self._build_as_numbered,
                              self.BuildMethod.MARKDOWN: self._build_as_markdown}
        artifact_params = DictUtil.update_kwarg_values(artifact_params, include_id=include_ids)
        self.artifact_params = artifact_params
        self.data_type = data_type
        self.starting_num = starting_num
        super().__init__(value=prompt_start, prompt_args=prompt_args)

    @overrides(Prompt)
    def _build(self, artifacts: List[EnumDict], structure: bool = True, **kwargs) -> str:
        """
        Builds the artifacts prompt using the given build method
        :param artifacts: The list of dictionaries containing the attributes representing each artifact.
        :param structure: Kept for API purposes.
        :param kwargs: Ignored.
        :return: The formatted prompt.
        """
        prompt = super()._build(structure=True, **kwargs)
        if self.build_method in self.build_methods:
            artifact_params = deepcopy(self.artifact_params)
            artifact_tokens = [TokenCalculator.estimate_num_tokens(artifact[ArtifactKeys.CONTENT]) for artifact in artifacts]
            if sum(artifact_tokens) > MAX_TOKENS_FOR_NO_SUMMARIES:
                artifact_params = DictUtil.update_kwarg_values(artifact_params, use_summary=True)
            artifacts = self.build_methods[self.build_method](artifacts,
                                                              starting_num=self.starting_num,
                                                              prompt=prompt,
                                                              artifact_params=artifact_params)
            return f"{prompt}{artifacts}" if artifacts else EMPTY_STRING
        else:
            raise NameError(f"Unknown Build Method: {self.build_method}")

    @staticmethod
    def _build_as_numbered(artifacts: List[EnumDict], artifact_params: Dict, starting_num: int = 1, **kwargs) -> str:
        """
        Formats the artifacts as follows:
        1. ID: BODY
        2. ID: BODY
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param artifact_params: Params to build artifact prompt with.
        :param include_ids: If True, includes artifact ids
        :param starting_num: Index to start counting from.
        :return: The formatted prompt
        """
        numbered_format = "{}. {}"
        artifact_prompt = ArtifactPrompt(build_method=ArtifactPrompt.BuildMethod.BASE, **artifact_params)
        formatted_artifacts = [numbered_format.format(i + starting_num, artifact_prompt.build(artifact=artifact, **kwargs))
                               for i, artifact in enumerate(artifacts)]
        return NEW_LINE.join(formatted_artifacts)

    @staticmethod
    def _build_as_xml(artifacts: List[ArtifactPrompt], artifact_params: Dict, **kwargs):
        """
        Formats the artifacts as follows:
        <artifact>
            <id>ID</id>
            <body>BODY</body>
        <artifact>
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param artifact_params: Parameters used to initialize artifact prompt
        :return: The formatted prompt
        """
        artifact_prompt = ArtifactPrompt(build_method=ArtifactPrompt.BuildMethod.XML, **artifact_params)
        formatted_artifacts = [artifact_prompt.build(artifact=artifact, **kwargs) for artifact in artifacts]
        return NEW_LINE.join(formatted_artifacts)

    @staticmethod
    def _build_as_markdown(artifacts: List[ArtifactPrompt], prompt: str, artifact_params: Dict, **kwargs):
        """
        Formats the artifacts as follows:
        # ID
        body
        :param artifacts: The list of dictionaries containing the attributes representing each artifact
        :param prompt: Determines header level. 1 if prompt not defined and 2 otherwise.
        :param artifact_params: The parameters to pass into artifact prompt construction.
        :param include_ids: If True, includes artifact ids
        :return: The formatted prompt
        """
        header_level = 1 if not prompt else 2
        artifact_prompt = ArtifactPrompt(build_method=ArtifactPrompt.BuildMethod.MARKDOWN, **artifact_params)
        formatted_artifacts = [artifact_prompt.build(artifact=artifact, header_level=header_level, **kwargs) for artifact in artifacts]
        return NEW_LINE.join(formatted_artifacts)

    def __repr__(self) -> str:
        """
        Returns a representation of the artifact prompt as a string
        :return: The artifact prompt as a string
        """
        if self.build_method.XML:
            return "<artifact>{artifact}<artifact> <artifact>{artifact}<artifact> ..."
        elif self.build_method.NUMBERED:
            return "1. {artifact1} " \
                   "2. {artifact2} ..."
