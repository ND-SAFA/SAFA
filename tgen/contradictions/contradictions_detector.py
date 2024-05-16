from typing import Dict, List

from tgen.common.objects.trace import Trace
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_result import ContradictionsResult
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys, TraceRelationshipType
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
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

    def detect(self, query_ids: List[str]) -> List[ContradictionsResult]:
        """
        Determines whether a given artifact has any contradictions
        :param query_ids: The id of the artifact to detect contradictions for.
        :return A list of ids that conflict with the artifact (empty list if none conflict) and the explanation for why.
        """
        assert all([q_id in self.args.dataset.artifact_df for q_id in query_ids]), f"Queries contain unknown ids: {query_ids}"
        results = []

        for query_id in query_ids:
            artifact_df = self.args.dataset.artifact_df
            id2context, all_relationships = ContextFinder.find_related_artifacts(query_id, self.args.dataset,
                                                                                 max_context=self.args.max_context,
                                                                                 base_export_dir=self.args.export_dir)
            trace_df = self.args.dataset.trace_dataset.trace_df if self.args.dataset.trace_dataset else TraceDataFrame()
            result = self._perform_detections(query_id, id2context)
            if not self.args.dataset.trace_dataset:
                artifact_type = artifact_df.get_artifact(query_ids)[ArtifactKeys.LAYER_ID]
                all_artifact_types = artifact_df.get_artifact_types()
                layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [artifact_type for _ in all_artifact_types],
                                           LayerKeys.TARGET_TYPE: all_artifact_types})
                self.args.dataset.trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)
            self.args.dataset.trace_dataset.trace_df = self._add_traces_to_df(all_relationships, trace_df)
            results.append(result)
        return results

    def _perform_detections(self, query_id: str, id2context: Dict[str, List[EnumDict]]) -> ContradictionsResult:
        """
        Performs the detection by prompting the LLM with the given context.
        :param query_id: The id of the artifact to perform detection on.
        :param id2context: Dictionary mapping query id to its related artifacts.
        :return: A list of ids that conflict with the artifact (empty list if none conflict) and the explanation for why.
        """
        prompt_builder, query_artifact, task_prompt = self.construct_prompt_builder(id2context, query_id)
        save_and_load_path = FileUtil.safely_join_paths(self.args.export_dir, f"{query_id}_contradictions_response.yaml")
        output = LLMTrainer.predict_from_prompts(self.args.llm_manager, prompt_builder,
                                                 save_and_load_path=save_and_load_path,
                                                 artifact=query_artifact)
        response = LLMResponseUtil.extract_predictions_from_response(output.predictions, task_prompt.args.prompt_id)[0]
        tags = task_prompt.get_all_response_tags()
        result = ContradictionsResult(**{tag: response[tag][0] if len(response[tag]) else None for tag in tags})
        self._filter_unknown_ids(result, id2context[query_id])
        return result

    def construct_prompt_builder(self, id2context, query_id):
        query_artifact = self.args.dataset.artifact_df.get_artifact(query_id)
        context_prompt = ContextPrompt(id2context, prompt_start=PromptUtil.as_markdown_header("Related Information"),
                                       build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN, include_ids=True)
        query_prompt = ArtifactPrompt(prompt_start=PromptUtil.as_markdown_header("Artifact"))
        instructions_prompt = Prompt(CONTRADICTIONS_INSTRUCTIONS)
        task_prompt: QuestionnairePrompt = SupportedPrompts.CONTRADICTIONS_TASK.value
        prompt_builder = PromptBuilder(prompts=[instructions_prompt, query_prompt, context_prompt, task_prompt])
        return prompt_builder, query_artifact, task_prompt

    @staticmethod
    def _filter_unknown_ids(result: ContradictionsResult, context_artifacts: List[EnumDict]) -> None:
        """
        Removes any artifact ids from the conflicting ids if they are unknown.
        :param result: The result from the contradictions detection.
        :param context_artifacts: Artifacts used for context for the expected artifact ids.
        :return: None.
        """
        expected_ids = {a[ArtifactKeys.ID] for a in context_artifacts}
        result["conflicting_ids"] = [a_id.strip() for a_id in result["conflicting_ids"] if a_id.strip() in expected_ids]

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
