from typing import List

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.objects.artifact import Artifact
from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.llm.prompts.artifact_prompt import ArtifactPrompt
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.llm.prompts.questionnaire_prompt import QuestionnairePrompt
from common_resources.tools.constants.default_model_managers import get_efficient_default_llm_manager

from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.chunkers.abstract_chunker import AbstractChunker
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class LLMChunker(AbstractChunker):

    def __init__(self, llm_manager: AbstractLLMManager = None):
        """
        Handles chunking artifacts using an llm.
        :param llm_manager: The llm to use for chunking.
        """
        self.llm_manager = get_efficient_default_llm_manager() if not llm_manager else llm_manager

    def chunk(self, artifacts2chunk: List[Artifact]) -> List[List[str]]:
        """
        Uses an LLM to chunk artifacts in dataframe into smaller chunks.
        :param artifacts2chunk: The artifacts to chunk.
        :return: List of the chunks.
        """
        task_prompt: QuestionnairePrompt = SupportedPrompts.CHUNK_INSTRUCTIONS.value
        prompt_builder = PromptBuilder([task_prompt, ArtifactPrompt(include_id=False,
                                                                    use_summary=True)])
        artifact_df = ArtifactDataFrame(artifacts2chunk)
        trainer_dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL:
                                                                                  PromptDataset(artifact_df=artifact_df)})
        trainer_state = LLMTrainerState(trainer_dataset_manager=trainer_dataset_manager,
                                        prompt_builders=prompt_builder,
                                        llm_manager=self.llm_manager)
        trainer = LLMTrainer(trainer_state)
        res = trainer.perform_prediction()
        chunks = [r[task_prompt.args.prompt_id][task_prompt.get_all_response_tags()[0]] for r in res.predictions]
        return chunks
