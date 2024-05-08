from typing import Any, List

from tgen.chat.message_meta import MessageMeta
from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.common.objects.artifact import Artifact
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, Message, PromptRoles
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
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
        for i, meta in enumerate(self.chat_history):
            if meta.artifact_ids or len(self.chat_history) == 1:
                self.add_context_to_message(meta, f"query_artifact_{i}")

        output = self.llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                          prompt=MessageMeta.to_llm_messages(self.chat_history))
        response: str = output.batch_responses[0]

        message = Message(content=response, role=PromptRoles.ASSISTANT)
        return MessageMeta(message=message, artifact_ids=self.chat_history[-1].artifact_ids)

    def add_context_to_message(self, message: MessageMeta, query_artifact_id: str) -> None:
        """
        Adds context to message.
        :param message: The message to extract context of.
        :param query_artifact_id: Unique ID to used to create an artifact to gather context for.
        :return: None
        """
        artifact_df: ArtifactDataFrame = self.job_args.dataset.artifact_df
        self.verify_no_unknown_artifacts(message, artifact_df)

        chat_content = message.message["content"]
        query_artifact = Artifact(id=query_artifact_id, content=chat_content, layer_id="query")
        id2context = self.extract_message_context(artifact_df, message, query_artifact)
        context_prompt = ContextPrompt(id2context,
                                       prompt_start=PromptUtil.as_markdown_header("Related Information"),
                                       build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                       include_ids=True)
        chat_prompt = Prompt(f"The related information is provided to help you better understand "
                             f"and respond to the following question. If you do not need the information to respond,"
                             f"you may ignore it."
                             f"{NEW_LINE * 2}`{chat_content}`", prompt_args=PromptArgs(title="Query"))
        prompt_str = PromptBuilder(prompts=[context_prompt, chat_prompt]).build(model_format_args=self.llm_manager.prompt_args,
                                                                                artifact=query_artifact)[PromptKeys.PROMPT]
        message.message["content"] = prompt_str

    def extract_message_context(self, artifact_df: ArtifactDataFrame, meta: MessageMeta, query_artifact: Artifact):
        """
        Extracts the artifacts related to the query.
        :param artifact_df: DataFrame containing artifacts to find for context.
        :param meta: Message containing optionally defined context artifacts.
        :param query_artifact: The query used to find which artifacts should be included in context.
        :return: Map of query ID to artifacts in context.
        """
        if meta.artifact_ids:
            id2context = {query_artifact[ArtifactKeys.ID]: [artifact_df.get_artifact(a_id) for a_id in meta.artifact_ids]}
        else:
            artifact_df.add_row(query_artifact)
            id2context, _ = ContextFinder.find_related_artifacts(query_artifact[ArtifactKeys.ID],
                                                                 self.job_args.dataset,
                                                                 base_export_dir=self.job_args.export_dir,
                                                                 max_context=self.max_context)
            meta.artifact_ids = [artifact[ArtifactKeys.ID] for artifact in id2context[query_artifact[ArtifactKeys.ID]]]
        return id2context

    @staticmethod
    def verify_no_unknown_artifacts(meta: MessageMeta, artifact_df: ArtifactDataFrame):
        """
        Verifies that all artifacts referenced in message are contained in dataframe.
        :param meta: Message whose artifacts are verified.
        :param artifact_df: Artifat Data Frame to contain artifacts.
        :return: None
        """
        unknown_ids = set(meta.artifact_ids).difference(artifact_df.index)
        assert not unknown_ids, f"Unknown artifact ids: {unknown_ids}"
