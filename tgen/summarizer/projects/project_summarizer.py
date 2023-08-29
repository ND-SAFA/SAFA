from tgen.common.constants.project_summary_constants import PROJECT_SUMMARY_TAGS, PS_QUESTIONS_HEADER
from tgen.common.constants.tracing.ranking_constants import BODY_ARTIFACT_TITLE, DEFAULT_SUMMARY_TOKENS
from tgen.common.util.base_object import BaseObject
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.project_summary_prompts import PROJECT_SUMMARY_CONTEXT_PROMPT
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.projects.project_summary import ProjectSummary
from tgen.summarizer.summarizer_args import SummarizerArgs


class ProjectSummarizer(BaseObject):

    def __init__(self, summarizer_args: SummarizerArgs, n_tokens: int = DEFAULT_SUMMARY_TOKENS):
        """
        Generates a system specification document for containing all artifacts.
        :param summarizer_args: The args necessary for the summary
        :param n_tokens: The token limit for the LLM
        """
        super().__init__()
        self.artifact_df = summarizer_args.dataset.artifact_df
        self.llm_manager: AbstractLLMManager = summarizer_args.llm_manager_for_project_summary
        self.n_tokens = n_tokens
        self.export_dir = summarizer_args.export_dir
        self.args = summarizer_args

    def summarize(self) -> str:
        """
        Creates the project summary from the project artifacts.
        :return: The summary of the project.
        """
        logger.log_title("Creating project specification.")

        if self.args.summarize_artifacts:
            self.artifact_df.summarize_content(ArtifactsSummarizer())

        project_summary = ProjectSummary(export_dir=self.export_dir, save_progress=True)
        for task_title, task_prompt in project_summary.get_generation_iterator():
            logger.log_step(f"Creating section: `{task_title}`")
            artifacts_prompt = MultiArtifactPrompt(prompt_prefix=BODY_ARTIFACT_TITLE,
                                                   build_method=MultiArtifactPrompt.BuildMethod.XML,
                                                   include_ids=True)
            prompt_builder = PromptBuilder(prompts=[PROJECT_SUMMARY_CONTEXT_PROMPT,
                                                    artifacts_prompt,
                                                    task_prompt])

            if project_summary.has_summary():
                current_summary = project_summary.get_summary()
                prompt_builder.add_prompt(Prompt(f"# Current Document\n\n{current_summary}"), 1)

            task_prompt.set_instructions(PS_QUESTIONS_HEADER)

            self.llm_manager.llm_args.set_max_tokens(self.n_tokens)
            self.llm_manager.llm_args.temperature = 0
            trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL:
                                                                                      PromptDataset(artifact_df=self.artifact_df)})
            trainer = LLMTrainer(LLMTrainerState(llm_manager=self.llm_manager,
                                                 prompt_builder=prompt_builder, trainer_dataset_manager=trainer_dataset_manager))
            task_tag = PROJECT_SUMMARY_TAGS[task_title]
            res = trainer.perform_prediction()
            id2res = prompt_builder.parse_responses(res.original_response[0])
            parsed_response = id2res[prompt_builder._prompts[-1].id][task_tag]

            task_body = parsed_response[0] if len(parsed_response) <= 1 else "\n".join(parsed_response)
            task_section = f"{PromptUtil.as_markdown_header(task_title)}\n{task_body}"
            task_section_body = task_section if len(task_section) == 0 else f"\n{task_section}"

            project_summary.set_section_body(task_title, task_section_body)
            project_summary.save()

        summary = project_summary.get_summary(raise_exception_on_not_found=True)
        return summary
