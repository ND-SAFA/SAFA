from typing import List

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.llm.llm_task import LLMCompletionType
from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.prompts.prompt_builder import PromptBuilder

from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState


def get_prediction_output(args: DeltaArgs, artifact_df: ArtifactDataFrame, state: DeltaState,
                          prompts: List[Prompt], **kwargs) -> List:
    """
    Gets the model predictions
    :param args: The arguments for the delta summarizer
    :param artifact_df: The artifacts to use in the prompts
    :param state: The current state of the delta summarizer
    :param prompts: The prompts to use for the predictions
    :return: The model predictions for each file diff
    """
    dataset = PromptDataset(artifact_df=artifact_df)
    dataset_manager = TrainerDatasetManager.create_from_datasets(eval=dataset)
    prompt_builder = PromptBuilder(prompts=prompts)
    prompt_builder.format_prompts_with_var(summary=state.project_summary.to_string(), **kwargs)
    trainer = LLMTrainer(LLMTrainerState(llm_manager=args.llm_manager,
                                         trainer_dataset_manager=dataset_manager,
                                         prompt_builders=prompt_builder,
                                         completion_type=LLMCompletionType.GENERATION))
    output = trainer.perform_prediction().predictions
    return output
