import os
import uuid
from typing import Tuple

from tgen.common.constants.deliminator_constants import NEW_LINE, COMMA
from tgen.common.constants.hgen_constants import TEMPERATURE_ON_RERUNS
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import HGenUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
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
            args.hgen_llm_manager_best.llm_args.temperature = TEMPERATURE_ON_RERUNS
        export_path = os.path.join(state.export_dir, filename) if state.export_dir else None

        task_prompt, target_tag_id, source_tag_id = self._create_task_prompt(args, state)
        generated_artifacts_tag, links_tag = task_prompt.response_manager.get_all_tag_ids()
        prompt_builder = HGenUtil.get_prompt_builder_for_generation(args, task_prompt,
                                                                    combine_summary_and_task_prompts=True)
        if state.summary:
            overview_of_system_prompt = Prompt(f"{PromptUtil.as_markdown_header('Overview of System:')}"
                                               f"{NEW_LINE}{state.summary}")
            prompt_builder.add_prompt(overview_of_system_prompt, 1)
        generation_predictions = HGenUtil.get_predictions(prompt_builder,
                                                          source_layer_only_dataset,
                                                          hgen_args=args,
                                                          prediction_step=PredictionStep.GENERATION,
                                                          response_prompt_ids={task_prompt.id},
                                                          tags_for_response={generated_artifacts_tag},
                                                          return_first=False,
                                                          export_path=export_path)[0]
        state.generation_predictions = {p[target_tag_id][0]: (p[source_tag_id][0] if len(p[source_tag_id]) > 0 else [])
                                        for p in generation_predictions if target_tag_id in p}
        state.n_generations += 1

    def _create_task_prompt(self, args: HGenArgs, state: HGenState) -> Tuple[QuestionnairePrompt, str, str]:
        """
        Creates the prompt used for the primary creation task
        :param args: The args to the hierarchy generator
        :param state: The current state of the hierarchy generator
        :return: The prompt used for the primary creation task
        """
        task_prompt = SupportedPrompts.HGEN_GENERATION_QUESTIONNAIRE.value
        task_prompt.id = self.TASK_PROMPT_ID
        target_type_tag, target_tag_id = HGenUtil.convert_spaces_to_dashes(args.target_type), "target"
        source_type_tag, source_tag_id = HGenUtil.convert_spaces_to_dashes(args.source_type), "source"
        task_prompt.response_manager = PromptResponseManager(
            response_instructions_format=f"Enclose each {args.target_type} in "
                                         + "{target}. Inside of the {target} tag, " +
                                         f"also include a comma-deliminated list of the ids for each {args.source_type} "
                                         f"from which you derived the {args.target_type} enclosed in " + "{source}",
            expected_responses={source_tag_id: set(state.source_dataset.artifact_df.index)},
            formatter=lambda tag, val: [v.strip() for v in val.split(COMMA)] if tag == source_tag_id
            else val.strip().strip(NEW_LINE),
            id2tag={target_tag_id: target_type_tag,
                    source_tag_id: source_type_tag},
            response_tag={target_type_tag: [source_type_tag]})
        task_prompt.format_value(format=state.format_of_artifacts, description=state.description_of_artifact)
        return task_prompt, target_tag_id, source_tag_id
