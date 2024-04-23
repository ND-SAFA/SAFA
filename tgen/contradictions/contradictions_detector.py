from typing import Dict, List, Optional

from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.objects.trace import Trace
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys, LayerKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.tracing.context_finder import ContextFinder


class ContradictionsDetector:

    def __init__(self, args: ContradictionsArgs):
        """
        Handles detecting contradictions in requirements.
        :param args: Arguments to the detector
        """
        self.args = args

    def detect(self, req_id: str) -> Optional[List[str]]:
        """
        Determines whether a given requirement has any contradictions
        :param req_id: The id of the requirement to detect contradictions for.
        :return
        """
        assert req_id in self.args.dataset.artifact_df, "Unknown requirement"

        artifact_df = self.args.dataset.artifact_df
        id2context, all_relationships = ContextFinder.find_related_artifacts(req_id, self.args.dataset,
                                                                             max_context=self.args.max_context,
                                                                             base_export_dir=self.args.export_dir)
        trace_df = self.args.dataset.trace_dataset.trace_df if self.args.dataset.trace_dataset else TraceDataFrame()
        conflicting_ids = self._perform_detections(req_id, id2context)
        if not self.args.dataset.trace_dataset:
            requirement_type = artifact_df.get_artifact(req_id)[ArtifactKeys.LAYER_ID]
            layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [requirement_type],
                                       LayerKeys.TARGET_TYPE: artifact_df.get_artifact_types()})
            self.args.dataset.trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
        self.args.dataset.trace_dataset.trace_df = self._add_traces_to_df(all_relationships, trace_df)
        return [a_id for a_id in conflicting_ids if a_id in artifact_df] if conflicting_ids else None

    def _perform_detections(self, req_id: str, id2context: Dict[str, List[EnumDict]]) -> Optional[List[str]]:
        """
        Performs the detection by prompting the LLM with the given context.
        :param req_id: The id of the requirement to perform detection on.
        :param id2context: Dictionary mapping requirement id to its related artifacts.
        :return: The output from the LLM.
        """
        requirement = self.args.dataset.artifact_df.get_artifact(req_id)
        context_prompt = ContextPrompt(id2context, prompt_start=PromptUtil.as_markdown_header("Related Information"),
                                       build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN, include_ids=True)
        requirement_prompt = ArtifactPrompt(prompt_start=PromptUtil.as_markdown_header("Requirement"))
        instructions_prompt = Prompt("Consider whether the following requirement is inconsistent or contradictory with any of the "
                                     "related pieces of information. ")
        task_prompt = Prompt("Output the ids of any contradictory or inconsistent information in a comma-deliminated list."
                             "If all the information entails or is neutral to the requirement, simply respond with no.",
                             title=f"Task",
                             response_manager=PromptResponseManager(response_tag="contradictions",
                                                                    value_formatter=self.format_response))
        prompt_builder = PromptBuilder(prompts=[instructions_prompt, requirement_prompt, context_prompt, task_prompt])
        save_and_load_path = FileUtil.safely_join_paths(self.args.export_dir, f"{req_id}_contradictions_response.yaml")
        output = LLMTrainer.predict_from_prompts(self.args.llm_manager, prompt_builder,
                                                 save_and_load_path=save_and_load_path,
                                                 artifact=requirement)
        response = LLMResponseUtil.extract_predictions_from_response(output.predictions, task_prompt.id,
                                                                     task_prompt.response_manager.response_tag, return_first=False)[0]
        return None if response[0] == CommonChoices.NO else response

    @staticmethod
    def format_response(tag: str, value: str) -> Optional[List[str]]:
        """
        Formats the LLM's response for the contradictions.
        :param tag: The name of the tag.
        :param value: The value of the response.
        :return: List of conflicting ids if there is a conflict, else None
        """
        conflicting_ids = value.split(COMMA)
        if len(conflicting_ids) == 1 and conflicting_ids[0].lower() == CommonChoices.NO:
            return CommonChoices.NO
        return conflicting_ids

    @staticmethod
    def _add_traces_to_df(selected_entries: List[Trace], trace_df: TraceDataFrame) -> TraceDataFrame:
        """
        Adds the selected traces to the dataframe.
        :param selected_entries: List of selected traces.
        :param trace_df: Dataframe to add to.
        :return: The dataframe containing selected traces.
        """
        for entry in selected_entries:
            entry[TraceKeys.LINK_ID] = TraceDataFrame.generate_link_id(entry[TraceKeys.SOURCE], entry[TraceKeys.TARGET])
        return TraceDataFrame.update_or_add_values(trace_df, selected_entries)
