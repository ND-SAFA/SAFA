from typing import Dict, List

from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder


def predict_artifact_prompt(artifact_content: str,
                            instructions_prompt: Prompt,
                            llm_manager: AbstractLLMManager) -> Dict:
    """
    Predicts the response from the LLM based on the artifact content and additional instructions.
    :param artifact_content: The content of the artifact.
    :param instructions_prompt: Instructions to append to the artifact content.
    :param llm_manager: LLM manager instance to use for predictions.
    :return: The parsed response from the LLM.
    """
    # Build the prompt
    artifact_prompt = Prompt(artifact_content, title="Artifact Content")

    # Combine prompts
    prompt_builder = PromptBuilder(prompts=[artifact_prompt, instructions_prompt])

    # Get prediction from the LLM
    output = LLMTrainer.predict_from_prompts(
        llm_manager,
        prompt_builder,
    )

    return output.predictions[0][instructions_prompt.id]


def predict_prompts(instruction_prompt: Prompt, content_prompts: List[str], llm_manager: AbstractLLMManager):
    prompts = [Prompt(p) for p in content_prompts] + [instruction_prompt]
    prompt_builder = PromptBuilder(prompts=prompts)

    # Get prediction from the LLM
    output = LLMTrainer.predict_from_prompts(
        llm_manager,
        prompt_builder,
    )

    return output.predictions[0][instruction_prompt.id]
