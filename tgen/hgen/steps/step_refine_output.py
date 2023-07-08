import os

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_util import _get_prompt_builder_for_generation, create_artifact_df_from_generated_artifacts, get_predictions
from tgen.util.logging.logger_manager import logger


def refine_artifact_content(hgen_args: HGenArgs) -> None:
    """
    Refines the artifact generation content.
    :param hgen_args: The arguments to HGEN and its current state.
    :return: None
    """
    generated_artifact_content = hgen_args.state.generated_artifact_content
    summary = hgen_args.state.summary
    export_path = hgen_args.state.export_path
    try:
        logger.info(f"Refining {len(generated_artifact_content)} {hgen_args.target_type}s\n")
        questionnaire = SupportedPrompts.HGEN_REFINE_QUESTIONNAIRE_CONTEXT.value
        prompt_builder = _get_prompt_builder_for_generation(hgen_args,
                                                            questionnaire,
                                                            base_prompt=SupportedPrompts.HGEN_REFINE_PROMPT_CONTEXT,
                                                            artifact_type=hgen_args.target_type)
        prompt_builder.add_prompt(Prompt(f"SUMMARY OF SYSTEM: {summary}"), 1)
        artifacts = create_artifact_df_from_generated_artifacts(hgen_args,
                                                                artifact_generations=generated_artifact_content,
                                                                target_layer_id=hgen_args.target_type,
                                                                generate_names=False)
        generated_artifacts_tag = questionnaire.question_prompts[-1].response_manager.response_tag
        refined_artifact_content = get_predictions(prompt_builder,
                                                   PromptDataset(artifact_df=artifacts),
                                                   hgen_args.hgen_llm_manager,
                                                   response_prompt_ids=questionnaire.id,
                                                   tags_for_response={generated_artifacts_tag},
                                                   return_first=True,
                                                   export_path=os.path.join(export_path, "gen_refinement_response1.yaml"))[0]


    except Exception:
        logger.exception("Refining the artifact content failed. Using original content instead.")
        refined_artifact_content = generated_artifact_content
    hgen_args.state.refined_content = refined_artifact_content
