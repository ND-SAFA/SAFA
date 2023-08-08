from copy import deepcopy

from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.delta.change_type import ChangeType
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class DiffSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):
    LAYER_ID = "diff"

    def run(self, args: DeltaArgs, state: DeltaState) -> None:
        modified_diffs = args.change_type_to_diffs[ChangeType.MODIFIED]
        original_artifacts = args.dataset.artifact_df
        ids = list(modified_diffs.keys())
        content = [SupportedPrompts.DELTA_CHANGED_FILE_PROMPT.value.format_value(
            original_artifacts.get_artifact(a_id)[ArtifactKeys.CONTENT], modified_diffs[a_id]) for a_id in ids]
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ids,
                                         ArtifactKeys.CONTENT: content,
                                         ArtifactKeys.LAYER_ID: [self.LAYER_ID for _ in ids]})
        diff_dataset = PromptDataset(artifact_df=artifact_df)
        dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: diff_dataset})
        prompt_builder = PromptBuilder(prompts=[SupportedPrompts.DELTA_PROJECT_SUMMARY_PROMPT.value,
                                                ArtifactPrompt(include_id=False),
                                                SupportedPrompts.DELTA_DIFF_SUMMARY_QUESTIONNAIRE.value])
        prompt_builder.format_prompts_with_var(summary=state.project_summary)
        trainer = LLMTrainer(LLMTrainerState(llm_manager=args.llm_manager,
                                             trainer_dataset_manager=dataset_manager,
                                             prompt_builder=prompt_builder,
                                             completion_type=LLMCompletionType.GENERATION))
        output = trainer.perform_prediction()
        output
