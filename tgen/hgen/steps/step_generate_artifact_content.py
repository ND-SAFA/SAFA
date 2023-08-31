import os
import uuid

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import convert_spaces_to_dashes, get_predictions, get_prompt_builder_for_generation
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class GenerateArtifactContentStep(AbstractPipelineStep[HGenArgs, HGenState]):
    TASK_PROMPT_ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'seed'))

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the content for the new artifacts.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        logger.info(f"Generating {args.target_type}s\n")

        source_layer_only_dataset = state.source_dataset
        filename = "artifact_gen_response"
        if state.n_generations > 0:
            filename = f"{filename}_{state.n_generations}"
            args.hgen_llm_manager_best.llm_args.temperature = 0.25
        export_path = os.path.join(state.export_dir, filename) if state.export_dir else None

        task_prompt = SupportedPrompts.HGEN_GENERATION_QUESTIONNAIRE.value
        task_prompt.id = self.TASK_PROMPT_ID
        task_prompt.response_manager = PromptResponseManager(
            response_instructions_format=f"Enclose each {args.target_type} in " + "{}",
            response_tag=convert_spaces_to_dashes(f"{args.target_type}"))
        task_prompt.format_value(format=state.format_of_artifacts, description=state.description_of_artifact)
        generated_artifacts_tag = task_prompt.response_manager.response_tag
        prompt_builder = get_prompt_builder_for_generation(args, task_prompt,
                                                           combine_summary_and_task_prompts=True)
        if state.summary:
            overview_of_system_prompt = Prompt(f"{PromptUtil.as_markdown_header('Overview of System:')}"
                                               f"{NEW_LINE}{state.summary}")
            prompt_builder.add_prompt(overview_of_system_prompt, 1)
        generation_predictions = get_predictions(prompt_builder,
                                                 source_layer_only_dataset,
                                                 hgen_args=args,
                                                 prediction_step=PredictionStep.GENERATION,
                                                 response_prompt_ids={task_prompt.id},
                                                 tags_for_response={generated_artifacts_tag},
                                                 return_first=False,
                                                 export_path=export_path)[0]
        state.generated_artifact_content = generation_predictions
        state.n_generations += 1
