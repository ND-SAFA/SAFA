from typing import List

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.llm.llm_task import LLMCompletionType
from gen_common.llm.llm_trainer import LLMTrainer
from gen_common.llm.llm_trainer_state import LLMTrainerState
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder

from gen.delta.delta_args import DeltaArgs
from gen.delta.delta_state import DeltaState


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
