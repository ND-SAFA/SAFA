from typing import List

from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.models.llm.llm_task import LLMCompletionType


def get_prediction_output(args: DeltaArgs, artifacts_df: ArtifactDataFrame, state: DeltaState,
                          prompts: List[Prompt], **kwargs) -> List:
    """
    Gets the model predictions
    :param args: The arguments for the delta summarizer
    :param artifacts_df: The artifacts to use in the prompts
    :param state: The current state of the delta summarizer
    :param prompts: The prompts to use for the predictions
    :return: The model predictions for each file diff
    """
    dataset = PromptDataset(artifact_df=artifacts_df)
    dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
    prompt_builder = PromptBuilder(prompts=prompts)
    prompt_builder.format_prompts_with_var(summary=state.project_summary, **kwargs)
    trainer = LLMTrainer(LLMTrainerState(llm_manager=args.llm_manager,
                                         trainer_dataset_manager=dataset_manager,
                                         prompt_builder=prompt_builder,
                                         completion_type=LLMCompletionType.GENERATION))
    output = trainer.perform_prediction().predictions
    return output
