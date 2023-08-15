import os

from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.hgen_prompts import SUMMARY_INSTRUCTIONS, TASK_INSTRUCTIONS
from tgen.hgen.hgen_args import HGenArgs, HGenState, PredictionStep
from tgen.hgen.hgen_util import convert_spaces_to_dashes, get_predictions, get_prompt_builder_for_generation, parse_generated_artifacts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class GenerateArtifactContentStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the content for the new artifacts.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        logger.info(f"Generating {args.target_type}s\n")
        summary_questionnaire = GenerateArtifactContentStep.construct_questionnaire_for_summary(state)

        source_layer_only_dataset = state.source_dataset
        export_path = os.path.join(state.export_path, "artifact_gen_response.yaml") if state.export_path else None

        task_prompt = QuestionPrompt(TASK_INSTRUCTIONS,
                                     response_manager=PromptResponseManager(
                                         response_instructions_format=f"Enclose each {args.target_type} in " + "{}",
                                         response_tag=convert_spaces_to_dashes(f"{args.target_type}"))

                                     )
        task_prompt.format_value(format=state.format_of_artifacts, description=state.description_of_artifact)
        summary_tag = summary_questionnaire.response_manager.response_tag
        generated_artifacts_tag = task_prompt.response_manager.response_tag
        prompt_builder = get_prompt_builder_for_generation(args, task_prompt, summary_prompt=summary_questionnaire,
                                                           combine_summary_and_task_prompts=True)
        task_prompt = prompt_builder.get_prompt(-1)
        if args.system_summary:
            overview_of_system_prompt = Prompt(f"{PromptUtil.format_as_markdown_header('Overview of System:')}"
                                               f"{NEW_LINE}{args.system_summary}")
            prompt_builder.add_prompt(overview_of_system_prompt, 1)
        generation_predictions = get_predictions(prompt_builder,
                                                 source_layer_only_dataset,
                                                 hgen_args=args,
                                                 prediction_step=PredictionStep.GENERATION,
                                                 response_prompt_ids={task_prompt.id},
                                                 tags_for_response={generated_artifacts_tag, summary_tag},
                                                 return_first=False,
                                                 export_path=export_path)[0]
        state.generated_artifact_content = generation_predictions[generated_artifacts_tag]
        if len(generation_predictions[summary_tag]) > 0:
            state.summary = generation_predictions[summary_tag][0]
        else:
            state.summary = EMPTY_STRING
            logger.warning("Failed to generate summary.")

    @staticmethod
    def construct_questionnaire_for_summary(state: HGenState) -> QuestionnairePrompt:
        """
        Constructs a questionnaire prompt that is used to generate the new artifacts
        :param state: The current hgen state
        :return: The questionnaire prompt that is used to generate the new artifacts
        """
        question_prompts = [QuestionPrompt(question) for i, question in enumerate(state.questions)]
        response_manager = PromptResponseManager(response_tag="summary")
        questionnaire_prompt = QuestionnairePrompt(question_prompts=question_prompts,
                                                   enumeration_chars=["-"],
                                                   instructions=SUMMARY_INSTRUCTIONS,
                                                   response_manager=response_manager)

        return questionnaire_prompt
