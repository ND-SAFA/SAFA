from typing import Dict, List, Tuple

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_result import ContradictionsResult
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys, TraceRelationshipType
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.contradiction_prompts import CONFLICTING_IDS_TAG, CONTRADICTIONS_INSTRUCTIONS, CONTRADICTION_TAG, \
    EXPLANATION_TAG
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.relationship_manager.cross_encoder_manager import CrossEncoderManager
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
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
        context_traces = []
        id2context = {}
        content_map = self.args.dataset.artifact_df.to_map()
        embeddings_manager = EmbeddingsManager(content_map=content_map)
        cross_encoder_manager = CrossEncoderManager(content_map=content_map)

        for query_id in query_ids:
            id2context_local, all_relationships = ContextFinder.find_related_artifacts(query_id, self.args.dataset,
                                                                                       max_context=self.args.max_context,
                                                                                       base_export_dir=self.args.export_dir,
                                                                                       embeddings_manager=embeddings_manager,
                                                                                       cross_encoder_manager=cross_encoder_manager)
            id2context.update(id2context_local)
            context_traces.extend(all_relationships)

        result = self._perform_detections(query_ids, id2context)

        if not self.args.dataset.trace_dataset:
            artifact_df = self.args.dataset.artifact_df
            trace_df = self.args.dataset.trace_dataset.trace_df if self.args.dataset.trace_dataset else TraceDataFrame()
            layer_df = self._create_layer_df(artifact_df, context_traces)
            self.args.dataset.trace_dataset = TraceDataset(artifact_df, trace_df, layer_df)

        self.args.dataset.trace_dataset.trace_df = self._add_traces_to_df(context_traces, self.args.dataset.trace_dataset.trace_df)
        return result

    def _perform_detections(self, query_ids: List[str], id2context: Dict[str, List[EnumDict]]) -> List[ContradictionsResult]:
        """
        Performs the detection by prompting the LLM with the given context.
        :param query_ids: The id of the artifact to perform detection on.
        :param id2context: Dictionary mapping query id to its related artifacts.
        :return: A list of ids that conflict with the artifact (empty list if none conflict) and the explanation for why.
        """
        prompts_global = []
        prompt_builders_global = []
        for query_id in query_ids:
            prompt_local, prompt_builder_local = self._construct_prompt_builder(id2context, query_id,
                                                                                self.args.llm_manager.prompt_args)
            prompts_global.append(prompt_local)
            prompt_builders_global.append(prompt_builder_local)

        save_and_load_path = FileUtil.safely_join_paths(self.args.export_dir, f"{query_id}_contradictions_response.yaml")
        output = LLMTrainer.predict_from_prompts(self.args.llm_manager,
                                                 prompt_builders=prompt_builders_global,
                                                 message_prompts=prompts_global,
                                                 save_and_load_path=save_and_load_path)

        results = []
        for output, prompt_builder, query_id in zip(output.predictions, prompt_builders_global, query_ids):
            task_prompt = prompt_builder.prompts[-1]
            parsed_output = output[task_prompt.args.prompt_id]
            for contradiction_dict in parsed_output[CONTRADICTION_TAG]:
                contradiction_explanation = contradiction_dict[EXPLANATION_TAG][0][0]
                contradicting_ids = contradiction_dict[CONFLICTING_IDS_TAG][0]
                result = ContradictionsResult(explanation=contradiction_explanation, conflicting_ids=contradicting_ids)
                self._filter_unknown_ids(result, id2context[query_id])
                result["conflicting_ids"] += [query_id]
                results.append(result)

        results = self._consolidate_results(results)

        return results

    def _construct_prompt_builder(self, id2context: Dict[str, List[Artifact]], query_id: str,
                                  prompt_args: LLMPromptBuildArgs) -> Tuple[Prompt, PromptBuilder]:
        """
        Creates the prompt builder used for detecting the contradictions.
        :param id2context: Maps artifact id to a list of related artifacts.
        :param query_id: ID of the artifact under investigation.
        :param prompt_args: The arguments to the prompt builder.
        :return: The constructed prompt and associated builder.
        """
        query_artifact = self.args.dataset.artifact_df.get_artifact(query_id)
        context_prompt = ContextPrompt(id2context, prompt_start=PromptUtil.as_markdown_header("Related Information"),
                                       build_method=MultiArtifactPrompt.BuildMethod.MARKDOWN, include_ids=True)
        query_prompt = ArtifactPrompt(prompt_start=PromptUtil.as_markdown_header("Artifact"))
        instructions_prompt = Prompt(CONTRADICTIONS_INSTRUCTIONS)
        task_prompt: QuestionnairePrompt = SupportedPrompts.CONTRADICTIONS_TASK.value
        prompt_builder = PromptBuilder(prompts=[instructions_prompt, query_prompt, context_prompt, task_prompt])
        prompt = prompt_builder.build(prompt_args, artifact=query_artifact)[PromptKeys.PROMPT]
        return prompt, prompt_builder

    @staticmethod
    def _consolidate_results(results: List[ContradictionsResult]) -> List[ContradictionsResult]:
        """
        Consolidate results by the artifact set they contradict with.
        :param results: List of contradictions found in set of artifacts.
        :return: List of contradictions each containing unique set of artifact ids.
        """
        result_group_table = {}
        for r in results:
            contradicting_id_hash = "*".join(sorted(set(r["conflicting_ids"])))  # TODO: Use better delimiter, curr is just unlikely
            DictUtil.initialize_value_if_not_in_dict(result_group_table, contradicting_id_hash, [])
            result_group_table[contradicting_id_hash].append(r)

        final_results = [results[0] for a_ids, results in result_group_table.items()]  # TODO : use LLM to consolidate messages.
        return final_results

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

    @staticmethod
    def _create_layer_df(artifact_df: ArtifactDataFrame, traces: List[Trace]) -> LayerDataFrame:
        """
        Creates Layer Data Frame containing layers identified in traces.
        :param artifact_df: DataFrame containing artifacts referenced in traces.
        :param traces: List of traces to extract layers from
        :return: LayerDataFrame.
        """
        layers = set()
        for t in traces:
            child_artifact = artifact_df.get_artifact(t[TraceKeys.child_label()])
            parent_artifact = artifact_df.get_artifact(t[TraceKeys.parent_label()])

            child_layer = child_artifact[ArtifactKeys.LAYER_ID]
            parent_layer = parent_artifact[ArtifactKeys.LAYER_ID]

            layers.add((child_layer, parent_layer))
        layer_df = LayerDataFrame([{LayerKeys.SOURCE_TYPE: s, LayerKeys.TARGET_TYPE: t}
                                   for s, t in layers])
        return layer_df
