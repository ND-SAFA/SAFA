from typing import Any, Dict, List

from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE

from tgen.common.constants.other_constants import DEFAULT_CONTEXT_THRESHOLD
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.override import overrides
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt


class ContextPrompt(MultiArtifactPrompt):

    def __init__(self, id_to_context_artifacts: Dict[Any, List[EnumDict]], **mult_artifact_prompt_args):
        """
        Creates a prompt that contains any additional context for the model, specifically related to a target artifact
        :param id_to_context_artifacts: An optional mapping of artifact id to a list of the related artifacts for context
        :param mult_artifact_prompt_args: Any additional arguments for formatting the multi artifact prompt
        """
        self.id_to_context_artifacts = id_to_context_artifacts
        super().__init__(**mult_artifact_prompt_args)

    @overrides(MultiArtifactPrompt)
    def _build(self, artifact: EnumDict, context_threshold: float = DEFAULT_CONTEXT_THRESHOLD, **kwargs) -> str:
        """
        Builds the artifacts prompt using the given build method
        :param artifact: The artifact to include in prompt.
        :param context_threshold: The similarity threshold for when to include similar content in context.
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        a_id = artifact[ArtifactKeys.ID]
        artifacts = self.id_to_context_artifacts.get(a_id, [])
        if artifacts:
            return super()._build(artifacts=artifacts, **kwargs) + NEW_LINE
        return EMPTY_STRING
