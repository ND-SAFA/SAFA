from typing import Any, Dict, List

from langchain_core.documents.base import Document

from gen_common.constants import EMPTY_STRING, NEW_LINE
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.util import EnumDict, ListUtil, default_mutable

DocumentType = str | Document


class ContextPrompt(MultiArtifactPrompt):

    @default_mutable()
    def __init__(self, id_to_context_artifacts: Dict[Any, List[EnumDict]] = None,
                 context_key: str = None, **mult_artifact_prompt_args):
        """
        Creates a prompt that contains any additional context for the model, specifically related to a target artifact
        :param id_to_context_artifacts: An optional mapping of artifact id to a list of the related artifacts for context
        :param context_key: The key associated with documents to retrieve for context when building prompt.
        :param mult_artifact_prompt_args: Any additional arguments for formatting the multi artifact prompt
        """
        self.context_key = context_key
        self.id_to_context_artifacts = id_to_context_artifacts if id_to_context_artifacts else {}
        super().__init__(**mult_artifact_prompt_args)

    @default_mutable()
    def _build(self, artifact: EnumDict = None, documents: List[DocumentType] | Dict[str, List[DocumentType]] = None, **kwargs) -> str:
        """
        Builds the artifacts prompt using the given build method
        :param artifact: The artifact to include in prompt.
        :param documents: List of documents to use as context.
        :param kwargs: Ignored
        :return: The formatted prompt
        """
        a_id = artifact[ArtifactKeys.ID] if artifact else None
        artifacts = self._get_relevant_context(documents=documents, a_id=a_id, **kwargs)

        if artifacts:
            return super()._build(artifacts=artifacts, **kwargs) + NEW_LINE
        return EMPTY_STRING

    def _get_relevant_context(self, documents: List[DocumentType] | Dict[str, List[DocumentType]],
                              a_id: str = None, **kwargs) -> List[Document]:
        """
        Gets the documents for this specific prompt based on the documents key (if provided)
        :param documents: The dictionary or list of context documents.
        :param a_id: The id of the specific artifact if id to context artifacts map is provided.
        :param kwargs: Additional arguments (may contain context as well).
        :return: The documents or an empty list of there are none.
        """
        context = []
        if self.context_key in kwargs:
            context = kwargs.get(self.context_key, [])
        elif isinstance(documents, dict):
            context = documents[self.context_key] if self.context_key else ListUtil.flatten(list(documents.values()))

        context = self._convert_to_artifacts(context)
        if self.id_to_context_artifacts:
            context.extend(self.id_to_context_artifacts.get(a_id, []))
        return context

    @staticmethod
    def _convert_to_artifacts(context: List[DocumentType | str | Artifact]) -> List[Artifact]:
        """
        Converts context items to the expected artifact type.
        :param context: List of documents, content strings or artifacts for context.
        :return: List of context items as artifacts.
        """
        artifacts = []
        for i, item in enumerate(context):
            if isinstance(item, Document):
                item = Artifact.convert_from_document(item)
            elif isinstance(item, str):
                item = Artifact(id=f"Document {i}", content=item)

            assert isinstance(item, EnumDict), f"Unknown context type: {type(item)}"
            artifacts.append(item)
        return artifacts
