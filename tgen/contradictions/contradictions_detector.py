from typing import Dict, List, Optional

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
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys, LayerKeys, TraceRelationshipType
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.contradiction_prompts import CONTRADICTIONS_INSTRUCTIONS
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.tracing.context_finder import ContextFinder


class ContradictionsDetector:

    def __init__(self, args: ContradictionsArgs):
        """
        Handles detecting contradictions in artifacts.
        :param args: Arguments to the detector
        """
        self.args = args

    def detect(self, query_id: str) -> Optional[List[str]]:
        """
        Determines whether a given artifact has any contradictions
        :param query_id: The id of the artifact to detect contradictions for.
        :return A list of ids that conflict with the artifact (empty list if none conflict)
        """
        assert query_id in self.args.dataset.artifact_df, "Unknown artifact"

        artifact_df = self.args.dataset.artifact_df
        id2context, all_relationships = ContextFinder.find_related_artifacts(query_id, self.args.dataset,
                                                                             max_context=self.args.max_context,
                                                                             base_export_dir=self.args.export_dir)
        trace_df = self.args.dataset.trace_dataset.trace_df if self.args.dataset.trace_dataset else TraceDataFrame()
        conflicting_ids = self._perform_detections(query_id, id2context)
        if not self.args.dataset.trace_dataset:
            artifact_type = artifact_df.get_artifact(query_id)[ArtifactKeys.LAYER_ID]
            all_artifact_types = artifact_df.get_artifact_types()
            layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [artifact_type for _ in all_artifact_types],
                                       LayerKeys.TARGET_TYPE: all_artifact_types})
            self.args.dataset.trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
        self.args.dataset.trace_dataset.trace_df = self._add_traces_to_df(all_relationships, trace_df)
        conflicting_ids = [a_id for a_id in conflicting_ids if a_id in artifact_df]
        return conflicting_ids if conflicting_ids else None

    def _perform_detections(self, query_id: str, id2context: Dict[str, List[EnumDict]]) -> Optional[List[str]]:
        """
        Performs the detection by prompting the LLM with the given context.
        :param query_id: The id of the artifact to perform detection on.
        :param id2context: Dictionary mapping query id to its related artifacts.
        :return: The output from the LLM.
        """
        query_artifact = self.args.dataset.artifact_df.get_artifact(query_id)
        context_prompt = ContextPrompt(id2context, prompt_start=PromptUtil.as_markdown_header("Related Information"),
                                       build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN, include_ids=True)
        query_prompt = ArtifactPrompt(prompt_start=PromptUtil.as_markdown_header("Artifact"))
        instructions_prompt = Prompt(CONTRADICTIONS_INSTRUCTIONS)
        task_prompt = SupportedPrompts.CONTRADICTIONS_TASK.value
        prompt_builder = PromptBuilder(prompts=[instructions_prompt, query_prompt, context_prompt, task_prompt])
        save_and_load_path = FileUtil.safely_join_paths(self.args.export_dir, f"{query_id}_contradictions_response.yaml")
        output = LLMTrainer.predict_from_prompts(self.args.llm_manager, prompt_builder,
                                                 save_and_load_path=save_and_load_path,
                                                 artifact=query_artifact)
        response = LLMResponseUtil.extract_predictions_from_response(output.predictions, task_prompt.id,
                                                                     task_prompt.response_manager.response_tag,
                                                                     return_first=False)[0][0]
        return None if response[0] == CommonChoices.NO else response

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
            if entry[TraceKeys.LINK_ID] not in trace_df:
                entry[TraceKeys.RELATIONSHIP_TYPE] = TraceRelationshipType.CONTEXT
        return TraceDataFrame.update_or_add_values(trace_df, selected_entries)
