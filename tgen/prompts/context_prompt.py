from typing import Any, Dict, List

from tgen.common.constants.other_constants import DEFAULT_CONTEXT_THRESHOLD
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingSorter


class ContextPrompt(MultiArtifactPrompt):

    def __init__(self, id_to_context_artifacts: Dict[Any, List[EnumDict]] = None, **mult_artifact_prompt_args):
        """
        Creates a prompt that contains any additional context for the model, specifically related to a target artifact
        :param id_to_context_artifacts: An optional mapping of artifact id to a list of the related artifacts for context
        :param mult_artifact_prompt_args: Any additional arguments for formatting the multi artifact prompt
        """
        self.id_to_context_artifacts = id_to_context_artifacts
        super().__init__(**mult_artifact_prompt_args)

    @overrides(MultiArtifactPrompt)
    def _build(self, artifact: EnumDict, embedding_manager: EmbeddingsManager = None,
               context_threshold: float = DEFAULT_CONTEXT_THRESHOLD, **kwargs) -> str:
        """
        Builds the artifacts prompt using the given build method
        :param artifact: The artifact to include in prompt.
        :param embedding_manager: The embedding manager used to calculate similar texts to include.
        :param context_threshold: The similarity threshold for when to include similar content in context.
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        a_id = artifact[ArtifactKeys.ID]
        id_to_context_artifacts = self.id_to_context_artifacts
        if not self.id_to_context_artifacts:
            assert embedding_manager is not None, "Must supply either a mapping of id to context or an embeddings manager to make one"
            embedding_manager.update_or_add_content(a_id, content=artifact[ArtifactKeys.CONTENT])
            sorted_entries = EmbeddingSorter.sort(parent_ids=[a_id],
                                                  child_ids=[id_ for id_ in embedding_manager.get_all_ids()
                                                             if id_ != a_id],
                                                  embedding_manager=embedding_manager, return_scores=True)
            embedding_manager.remove_artifacts(a_id)
            sorted_ids, scores = sorted_entries[a_id]
            id_to_context_artifacts = {a_id: [EnumDict({ArtifactKeys.ID: id_,
                                                        ArtifactKeys.CONTENT: embedding_manager.get_content(id_)})
                                              for id_, score in zip(sorted_ids, scores) if score >= context_threshold]}
        artifacts = id_to_context_artifacts.get(a_id)
        return super()._build(artifacts=artifacts, **kwargs)
