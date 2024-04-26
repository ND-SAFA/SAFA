from typing import Any, Dict, List

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, CONTENT_KEY
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.tracing.context_finder import ContextFinder


class ChatJob(AbstractJob):

    def __init__(self, job_args: JobArgs, chat_history: List[Dict[str, str]], llm_manager: AbstractLLMManager = None,
                 max_context: int = None):
        """
        Initializes the job with the previous chats.
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
        related_artifacts = None
        if len(self.chat_history) == 1:
            artifact_df: ArtifactDataFrame = self.job_args.dataset.artifact_df
            chat_content = self.chat_history[0][CONTENT_KEY]
            artifact_id = "query_artifact"
            query_artifact = artifact_df.add_artifact(id=artifact_id, content=chat_content, layer_id="chat")
            id2context, related_traces = ContextFinder.find_related_artifacts(artifact_id, self.job_args.dataset,
                                                                              base_export_dir=self.job_args.export_dir,
                                                                              max_context=self.max_context)
            context_prompt = ContextPrompt(id2context,
                                           prompt_start=PromptUtil.as_markdown_header("Related Information"),
                                           build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN,
                                           include_ids=True)
            chat_prompt = Prompt(f"Use the related information to better understand and respond to the following question: "
                                 f"{NEW_LINE}{chat_content}", title="Query")
            prompt_str = PromptBuilder(prompts=[context_prompt, chat_prompt]).build(model_format_args=self.llm_manager.prompt_args,
                                                                                    artifact=query_artifact)[PromptKeys.PROMPT]
            related_artifacts = id2context[artifact_id]
            self.chat_history[0][CONTENT_KEY] = prompt_str

        output = self.llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                          prompt=self.chat_history)
        response = output.batch_responses[0]
        return response, related_artifacts
