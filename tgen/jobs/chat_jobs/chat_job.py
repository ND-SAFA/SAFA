from typing import Any, List, Set

from tgen.chat.message_meta import MessageMeta
from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.common.objects.artifact import Artifact
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, Message, PromptRoles
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.tracing.context_finder import ContextFinder


class ChatJob(AbstractJob):

    def __init__(self, job_args: JobArgs, chat_history: List[MessageMeta], llm_manager: AbstractLLMManager = None,
                 max_context: int = None):
        """
        Initializes the job with the previous chats.
        :param job_args: Contains dataset and other common arguments to jobs in general.
        :param chat_history: List containing previous conversation, with the last item containing most recent user query.
        :param llm_manager: Responsible for making LLM responses.
        :param max_context: The max number of artifacts to include in the context for the model.
        """
        super().__init__(job_args, require_data=True)
        self.chat_history = chat_history
        self.llm_manager = get_best_default_llm_manager_long_context() if not llm_manager else llm_manager
        self.max_context = max_context

    def _run(self) -> Any:
        """
        Runs the job to get the next response from the LLM.
        :return: The next response from the LLM.
        """
        artifact_df: ArtifactDataFrame = self.job_args.dataset.artifact_df
        current_context = self.identify_context_artifacts(artifact_df)
        system_prompt = self.create_system_prompt(current_context, artifact_df)
        message = self.get_llm_response(system_prompt)
        return MessageMeta(message=message, artifact_ids=self.chat_history[-1].artifact_ids)

    def get_llm_response(self, system_prompt: str) -> Message:
        """
        Sends the chat to the LLM to get a response.
        :param system_prompt: Contains the context for the chat.
        :return: The message from the LLM.
        """
        output = self.llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                          prompt=MessageMeta.to_llm_messages(self.chat_history),
                                                          system=[system_prompt])
        response: str = output.batch_responses[0]
        message = Message(content=response, role=PromptRoles.ASSISTANT)
        return message

    def identify_context_artifacts(self, artifact_df: ArtifactDataFrame) -> Set[str]:
        """
        Identifies what artifacts should be shown in the context.
        :param artifact_df: Contains the project artifacts.
        :return: A set of artifact ids to use for context.
        """
        current_context = set()
        for i, meta in enumerate(self.chat_history):
            self.verify_no_unknown_artifacts(meta, artifact_df)
            if not meta.artifact_ids:
                self.add_related_context(artifact_df, meta, f"query_artifact_{i}")
            current_context.update(meta.artifact_ids)
        return current_context

    def create_system_prompt(self, context_artifact_ids: Set[str], artifact_df: ArtifactDataFrame) -> str:
        """
        Adds context to message.
        :param context_artifact_ids: The list of artifact ids to use for context.
        :param artifact_df: Contains the project artifacts.
        :return: The system's prompt string for the context.
        """
        context_artifacts = [artifact_df.get_artifact(a_id) for a_id in context_artifact_ids]
        context_prompt = MultiArtifactPrompt(prompt_start=f"The related information is provided to help you better understand "
                                                          f"and respond to the following question. "
                                                          f"If you do not need the information to respond,"
                                                          f"you may ignore it.",
                                             prompt_args=PromptArgs(title="Related Information", system_prompt=True),
                                             build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                             include_ids=True)
        prompt_str = PromptBuilder(prompts=[context_prompt]).build(model_format_args=self.llm_manager.prompt_args,
                                                                   artifacts=context_artifacts)[PromptKeys.SYSTEM]
        return prompt_str

    def add_related_context(self, artifact_df: ArtifactDataFrame, meta: MessageMeta,
                            query_artifact_id: str) -> None:
        """
        Extracts the artifacts related to the query.
        :param artifact_df: DataFrame containing artifacts to find for context.
        :param meta: Message containing optionally defined context artifacts.
        :param query_artifact_id: The id of the query used to find which artifacts should be included in context.
        :return: None - updates the meta artifact_ids for context.
        """
        chat_content = meta.message["content"]
        query_artifact = Artifact(id=query_artifact_id, content=chat_content, layer_id="query")
        artifact_df.add_row(query_artifact)
        id2context, _ = ContextFinder.find_related_artifacts(query_artifact[ArtifactKeys.ID],
                                                             self.job_args.dataset,
                                                             base_export_dir=self.job_args.export_dir,
                                                             max_context=self.max_context)
        artifact_df.remove_row(query_artifact[ArtifactKeys.ID])
        meta.artifact_ids = [artifact[ArtifactKeys.ID] for artifact in id2context[query_artifact[ArtifactKeys.ID]]]

    @staticmethod
    def verify_no_unknown_artifacts(meta: MessageMeta, artifact_df: ArtifactDataFrame) -> None:
        """
        Verifies that all artifacts referenced in message are contained in dataframe.
        :param meta: Message whose artifacts are verified.
        :param artifact_df: Artifact Data Frame to contain artifacts.
        :return: None
        """
        unknown_ids = set(meta.artifact_ids).difference(artifact_df.index)
        assert not unknown_ids, f"Unknown artifact ids: {unknown_ids}"
