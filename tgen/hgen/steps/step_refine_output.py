import os
from typing import List, Tuple, Dict

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, HGenState
from tgen.hgen.hgen_util import _get_prompt_builder_for_generation, create_artifact_df_from_generated_artifacts, get_predictions
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.util.logging.logger_manager import logger


class RefineArtifactContent(AbstractPipelineStep[HGenArgs, HGenState]):
    def run(self, hgen_args: HGenArgs, state: HGenState) -> None:
        """
        Refines the artifact generation content.
        :param hgen_args: The arguments to HGEN and its current state.
        :return: None
        """
        generated_artifact_content = state.generated_artifact_content
        summary = state.summary
        export_path = state.export_path
        refinement_questionnaire = state.refinement_questionnaire

        generated_artifacts_tag, refined_artifact_content = RefineArtifactContent.perform_refinement(hgen_args,
                                                                                                     generated_artifact_content,
                                                                                                     refinement_questionnaire,
                                                                                                     summary,
                                                                                                     export_path)
        state.refined_content = refined_artifact_content[generated_artifacts_tag]

    @staticmethod
    def perform_refinement(hgen_args: HGenArgs,
                           generated_artifact_content: List[str],
                           questionnaire: QuestionnairePrompt,
                           summary: str,
                           export_path: str):
        try:
            logger.info(f"Refining {len(generated_artifact_content)} {hgen_args.target_type}s\n")
            prompt_builder = _get_prompt_builder_for_generation(hgen_args,
                                                                questionnaire,
                                                                base_prompt=SupportedPrompts.HGEN_REFINE_PROMPT_CONTEXT,
                                                                artifact_type=hgen_args.target_type)
            prompt_builder.add_prompt(Prompt(f"SUMMARY OF SYSTEM: {summary}"), 1)
            artifacts = create_artifact_df_from_generated_artifacts(hgen_args,
                                                                    artifact_generations=generated_artifact_content,
                                                                    target_layer_id=hgen_args.target_type,
                                                                    generate_names=False)
            generated_artifacts_tag: str = questionnaire.question_prompts[-1].response_manager.response_tag
            refined_artifact_content = get_predictions(prompt_builder,
                                                       PromptDataset(artifact_df=artifacts),
                                                       hgen_args.hgen_llm_manager,
                                                       hgen_args.refinement_tokens,
                                                       response_prompt_ids=questionnaire.id,
                                                       tags_for_response={generated_artifacts_tag},
                                                       return_first=True,
                                                       export_path=os.path.join(export_path, "gen_refinement_response1.yaml"))[0]


        except Exception:
            logger.exception("Refining the artifact content failed. Using original content instead.")
            refined_artifact_content = generated_artifact_content
        return generated_artifacts_tag, refined_artifact_content


def perform_refinement(hgen_args: HGenArgs,
                       generated_artifact_content: List[str],
                       questionnaire: QuestionnairePrompt,
                       summary: str,
                       export_path: str) -> Tuple[str, Dict]:
    """
    Performs the refinement of the original generated artifact content
    :param hgen_args: The arguments for the hierarchy generation
    :param generated_artifact_content: The content originally generated
    :param questionnaire: The questionnaire containing the refinement steps
    :param summary: The summary of the system
    :param export_path: The path to export the checkpoint to
    :return: The tag to retrieve the refinements and the refined content
    """
    generated_artifacts_tag: str = questionnaire.question_prompts[-1].response_manager.response_tag
    try:
        logger.info(f"Refining {len(generated_artifact_content)} {hgen_args.target_type}s\n")
        prompt_builder = _get_prompt_builder_for_generation(hgen_args,
                                                            questionnaire,
                                                            base_prompt=SupportedPrompts.HGEN_REFINE_PROMPT_CONTEXT,
                                                            artifact_type=hgen_args.target_type)
        prompt_builder.add_prompt(Prompt(f"SUMMARY OF SYSTEM: {summary}"), 1)
        artifacts = create_artifact_df_from_generated_artifacts(hgen_args,
                                                                artifact_generations=generated_artifact_content,
                                                                target_layer_id=hgen_args.target_type,
                                                                generate_names=False)
        refined_artifact_content = get_predictions(prompt_builder,
                                                   PromptDataset(artifact_df=artifacts),
                                                   hgen_args.hgen_llm_manager,
                                                   hgen_args.refinement_tokens,
                                                   response_prompt_ids=questionnaire.id,
                                                   tags_for_response={generated_artifacts_tag},
                                                   return_first=True,
                                                   export_path=os.path.join(export_path, "gen_refinement_response1.yaml"))[0]


    except Exception:
        logger.exception("Refining the artifact content failed. Using original content instead.")
        refined_artifact_content = generated_artifact_content
    return generated_artifacts_tag, refined_artifact_content
