import os

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_util import _convert_spaces_to_dashes, _get_prompt_builder_for_generation, get_predictions
from tgen.util.logging.logger_manager import logger


def generate_artifact_content(hgen_args: HGenArgs) -> None:
    """
    Creates the content for the new artifacts.
    :param hgen_args: The arguments and current state of the run.
    :return: None
    """
    logger.info(f"Generating {hgen_args.target_type}s\n")

    source_layer_only_dataset = hgen_args.state.source_dataset
    export_path = hgen_args.state.export_path
    format_of_artifacts = hgen_args.format_of_artifacts
    summary_questionnaire = hgen_args.state.generation_questionnaire

    task_prompt = Prompt("Then, reverse engineer as many {target_type}s as possible for the {source_type}. "
                         "Each {target_type} should use the following format '{format}'. "
                         "Enclose all {target_type}s in a comma deliminated list. ",
                         response_manager=PromptResponseManager(
                             response_tag=_convert_spaces_to_dashes(hgen_args.target_type))

                         )
    task_prompt.format_value(format=format_of_artifacts)
    prompt_builder = _get_prompt_builder_for_generation(task_prompt, summary_prompt=summary_questionnaire)
    summary_tag = summary_questionnaire.response_manager.response_tag
    generated_artifacts_tag = task_prompt.response_manager.response_tag
    generation_predictions = get_predictions(prompt_builder, source_layer_only_dataset,
                                             response_prompt_ids={task_prompt.id, summary_questionnaire.id},
                                             tags_for_response={generated_artifacts_tag, summary_tag},
                                             return_first=True,
                                             export_path=os.path.join(export_path, "artifact_gen_response.yaml"))[0]
    generated_artifact_content = generation_predictions[generated_artifacts_tag]
    summary = generation_predictions[summary_tag]

    hgen_args.state.generated_artifact_content = generated_artifact_content
    hgen_args.state.summary = summary
