from tgen.common.constants.ranking_constants import BODY_ARTIFACT_TITLE, DEFAULT_SUMMARY_TOKENS
from tgen.common.util.base_object import BaseObject
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


class ProjectSummarizer(BaseObject):

    def __init__(self, summarizer_args: SummarizerArgs, n_tokens: int = DEFAULT_SUMMARY_TOKENS):
        """
        Generates a system specification document for containing all artifacts.
        :param summarizer_args: The args necessary for the summary
        :param n_tokens: The token limit for the LLM
        """
        super().__init__()
        self.artifacts_df = summarizer_args.dataset.artifact_df
        self.llm_manager: AbstractLLMManager = summarizer_args.llm_manager_for_project_summary
        self.n_tokens = n_tokens
        self.export_path = summarizer_args.export_dir

    def summarize(self) -> str:
        """
        Creates the summary
        :return: The summary of the project
        """
        logger.log_title("Creating project specification.")

        self.artifacts_df.summarize_content(ArtifactsSummarizer())

        task_prompt: QuestionnairePrompt = SupportedPrompts.PROJECT_SUMMARY.value
        artifacts_prompt = MultiArtifactPrompt(prompt_prefix=BODY_ARTIFACT_TITLE,
                                               build_method=MultiArtifactPrompt.BuildMethod.XML,
                                               include_ids=True)
        prompt_builder = PromptBuilder(prompts=[task_prompt, artifacts_prompt])

        self.llm_manager.llm_args.set_max_tokens(self.n_tokens)
        self.llm_manager.llm_args.temperature = 0
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL:
                                                                                  PromptDataset(artifact_df=self.artifacts_df)})
        trainer = LLMTrainer(LLMTrainerState(llm_manager=self.llm_manager,
                                             prompt_builder=prompt_builder, trainer_dataset_manager=trainer_dataset_manager))
        res = trainer.perform_prediction()
        summary = res.predictions[0][task_prompt.id][task_prompt.response_manager.response_tag]
        summary = res.original_response[0] if len(summary) == 0 else summary[0]
        if self.export_path:
            FileUtil.write(summary, self.export_path)
        return summary
