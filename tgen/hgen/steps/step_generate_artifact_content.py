import os

from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_util import _get_prompt_builder_for_generation, get_predictions
from tgen.util.logging.logger_manager import logger


def generate_artifact_content(hgen_args: HGenArgs) -> None:
    """
    Creates the content for the new artifacts.
    :param hgen_args: The arguments and current state of the run.
    :return: None
    """
    logger.info(f"Generating {hgen_args.target_type}s\n")

    questionnaire = hgen_args.state.questionnaire
    source_layer_only_dataset = hgen_args.state.source_dataset
    export_path = hgen_args.state.export_path

    prompt_builder = _get_prompt_builder_for_generation(hgen_args, questionnaire, include_summary=True)
    summary_tag = prompt_builder.get_prompt(-2).response_manager.response_tag
    generated_artifacts_tag = questionnaire.question_prompts[-1].response_manager.response_tag
    generation_predictions = get_predictions(prompt_builder,
                                             source_layer_only_dataset,
                                             hgen_args.hgen_llm_manager,
                                             response_prompt_ids=questionnaire.id,
                                             tags_for_response={generated_artifacts_tag, summary_tag},
                                             return_first=True,
                                             export_path=os.path.join(export_path, "artifact_gen_response.yaml"))[0]
    generated_artifact_content = generation_predictions[generated_artifacts_tag]
    summary = generation_predictions[summary_tag]

    hgen_args.state.generated_artifact_content = generated_artifact_content
    hgen_args.state.summary = summary
