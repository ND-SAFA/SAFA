import math
import os
from unittest.mock import MagicMock

import mock
import pandas as pd

from test.hgen.hgen_test_utils import HGenTestConstants, get_generated_artifacts_response, get_name_responses, get_predictions, \
    get_test_hgen_args, HGEN_PROJECT_SUMMARY, MISSING_PROJECT_SUMMARY_RESPONSES
from test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.pipeline_util import PipelineUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.hgen.steps.step_generate_trace_links import GenerateTraceLinksStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_refine_generations import RefineGenerationsStep
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_libraries import mock_libraries
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep


class TestHierarchyGenerator(BaseTest):
    HGEN_ARGS = None
    HGEN_STATE = HGenState()

    @mock_anthropic
    def test_run(self, anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.mock_summarization()
        self.HGEN_ARGS = get_test_hgen_args(test_refinement=True)()
        self.HGEN_ARGS.dataset.project_summary = HGEN_PROJECT_SUMMARY
        self.HGEN_STATE.export_dir = self.HGEN_ARGS.export_dir
        self.assert_initialize_dataset_step()
        self.assert_generate_input_step()
        self.assert_generate_artifact_content_step()
        self.assert_refined_artifact_content_step()
        self.assert_generate_trace_links_step()
        self.assert_create_dataset_step()
        self.assert_save_dataset_checkpoint()

    def assert_save_dataset_checkpoint(self):
        def assert_dataset(dataset: TraceDataset, orig_dataset: TraceDataset):
            self.assertSetEqual(set(dataset.artifact_df.index), set(orig_dataset.artifact_df.index))
            self.assertEqual(len(dataset.trace_df), len(orig_dataset.trace_df))
            for i, trace in orig_dataset.trace_df.itertuples():
                self.assertIsNotNone(dataset.trace_df.get_link(source_id=trace[TraceKeys.SOURCE], target_id=trace[TraceKeys.TARGET]))
            self.assertEqual(len(dataset.layer_df), len(orig_dataset.layer_df))

        export_path = TEST_OUTPUT_DIR
        safa_save_path = PipelineUtil.save_dataset_checkpoint(self.HGEN_STATE.final_dataset, export_path, filename="dir",
                                                              exporter_class=SafaExporter)
        saved_safa_dataset = TraceDatasetCreator(StructuredProjectReader(project_path=safa_save_path)).create()
        assert_dataset(saved_safa_dataset, self.HGEN_STATE.final_dataset)
        csv_save_path = PipelineUtil.save_dataset_checkpoint(self.HGEN_STATE.source_dataset, export_path, filename="artifacts")
        saved_csv_dataset = ArtifactDataFrame(pd.read_csv(csv_save_path))
        self.assertSetEqual(set(saved_csv_dataset.index), set(self.HGEN_STATE.source_dataset.artifact_df.index))
        dataframe_save_path = PipelineUtil.save_dataset_checkpoint(self.HGEN_STATE.original_dataset, export_path, filename="dir")
        saved_dataframe_dataset = TraceDatasetCreator(DataFrameProjectReader(project_path=dataframe_save_path)).create()
        assert_dataset(saved_dataframe_dataset, self.HGEN_STATE.original_dataset)
        non_dataset = {"hello": "world"}
        yaml_save_path = PipelineUtil.save_dataset_checkpoint(non_dataset, export_path, filename="non_dataset")
        yaml_content = FileUtil.read_yaml(yaml_save_path)
        self.assertDictEqual(non_dataset, yaml_content)

    def assert_initialize_dataset_step(self):
        # contains a project summary but no artifact summaries so artifacts are summarized while project is not
        InitializeDatasetStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        for id_, artifact in self.HGEN_STATE.source_dataset.artifact_df.itertuples():
            self.assertEqual(artifact[ArtifactKeys.LAYER_ID], "C++ Code")

    @mock_libraries
    def assert_generate_input_step(self, anthropic_ai_manager: TestAIManager, openai_ai_manager: TestAIManager):
        anthropic_ai_manager.set_responses(HGenTestConstants.responses_inputs)
        openai_ai_manager.set_responses(HGenTestConstants.open_ai_responses)

        step = GenerateInputsStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        path = step._get_inputs_save_path(target_type=self.HGEN_ARGS.target_type, source_type=self.HGEN_ARGS.source_type)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(self.HGEN_STATE.description_of_artifact, HGenTestConstants.description)
        self.assertEqual(self.HGEN_STATE.format_of_artifacts, HGenTestConstants.format_)
        self.assertEqual(self.HGEN_STATE.questions, HGenTestConstants.questions.split("\n"))
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        os.remove(path)
        self.assertEqual(openai_ai_manager.n_used, 1)
        self.assertEqual(anthropic_ai_manager.n_used, 1)

    @mock_anthropic
    def assert_generate_artifact_content_step(self, anthropic_ai_manager: TestAIManager):
        self.HGEN_ARGS.target_type = "User Story"
        response = get_generated_artifacts_response()
        anthropic_ai_manager.set_responses(response)
        step = GenerateArtifactContentStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for i, us in enumerate(self.HGEN_STATE.generation_predictions.keys()):
            self.assertEqual(us, HGenTestConstants.user_stories[i])
            self.assertEqual(set(self.HGEN_STATE.generation_predictions[us]), set(HGenTestConstants.code_files[i]))

    @mock_anthropic
    def assert_refined_artifact_content_step(self, anthropic_ai_manager: TestAIManager):
        refined_user_stories1 = ["#1" + us for us in HGenTestConstants.user_stories]
        refined_user_stories2 = ["#2" + us for us in HGenTestConstants.user_stories]
        refine_response1 = [PromptUtil.create_xml("selected-artifacts", "1,5,6")]  # orig content no. 1 and refined us #1 no. 2,3
        refine_response2 = [PromptUtil.create_xml("selected-artifacts", "1,2,6")]  # orig content no. 1, refined no. 2 (#1) and 3 (#2)
        anthropic_ai_manager.set_responses(get_generated_artifacts_response(contents=refined_user_stories1)
                                           + refine_response1
                                           + get_generated_artifacts_response(contents=refined_user_stories2)
                                           + refine_response2
                                           )
        self.HGEN_ARGS.perform_clustering = False
        RefineGenerationsStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        us1 = HGenTestConstants.user_stories[0]
        us2 = refined_user_stories1[1]
        us3 = refined_user_stories2[2]
        for i, us in enumerate([us1, us2, us3]):
            self.assertIn(us, self.HGEN_STATE.refined_content)
            self.assertEqual(set(self.HGEN_STATE.refined_content[us]), set(HGenTestConstants.code_files[i]))

    @mock_anthropic
    @mock.patch.object(CreateExplanationsStep, "run")
    @mock.patch.object(CompleteRankingPromptsStep, "complete_ranking_prompts")
    def assert_generate_trace_links_step(self, anthropic_ai_manager: TestAIManager, ranking_mock: MagicMock,
                                         explanation_mock: MagicMock):
        names, expected_names, responses = get_name_responses(self.HGEN_STATE.generation_predictions)
        responses.extend(MISSING_PROJECT_SUMMARY_RESPONSES)
        anthropic_ai_manager.set_responses(responses)
        anthropic_ai_manager.mock_summarization()
        predictions = get_predictions(expected_names, self.HGEN_STATE.source_dataset.artifact_df.index)
        ranking_mock.return_value = predictions
        step = GenerateTraceLinksStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for name in expected_names:
            self.assertIn(name, list(self.HGEN_STATE.all_artifacts_dataset.artifact_df.index))
        us2code = {us: code for us, code in zip(expected_names, HGenTestConstants.code_files)}
        for new_pred in self.HGEN_STATE.trace_predictions:
            parent = new_pred[TraceKeys.parent_label()]
            child = new_pred[TraceKeys.child_label()]
            if child in us2code[parent]:
                self.assertGreater(new_pred[TraceKeys.SCORE], 0.8)  # these should be weighted higher than original prediction

    def assert_create_dataset_step(self):
        step = CreateHGenDatasetStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for id_, link in self.HGEN_STATE.original_dataset.trace_dataset.trace_df.itertuples():
            found_link = self.HGEN_STATE.final_dataset.trace_df.get_link(source_id=link[TraceKeys.SOURCE],
                                                                         target_id=link[TraceKeys.TARGET])
            self.assertIsNotNone(found_link)
        for content in self.HGEN_STATE.refined_content.keys():
            name = self.HGEN_STATE.final_dataset.artifact_df.filter_by_row(lambda row:
                                                                           row[ArtifactKeys.CONTENT.value] == content).index[0]
            new_artifact = self.HGEN_STATE.final_dataset.artifact_df.get_artifact(name)
            self.assertEqual(new_artifact[ArtifactKeys.LAYER_ID], self.HGEN_ARGS.target_type)
            for orig_id, orig_artifact in self.HGEN_STATE.original_dataset.artifact_df.itertuples():
                self.assertIn(orig_id, self.HGEN_STATE.final_dataset.artifact_df.index)
                if orig_artifact[ArtifactKeys.LAYER_ID] == self.HGEN_ARGS.source_layer_id:
                    q = DataFrameUtil.query_df(self.HGEN_STATE.final_dataset.trace_df, {"source": orig_id, "target": name})
                    self.assertEqual(len(q), 1)
        for i, layer in self.HGEN_STATE.original_dataset.trace_dataset.layer_df.itertuples():
            q = DataFrameUtil.query_df(self.HGEN_STATE.final_dataset.layer_df, layer)
            self.assertEqual(len(q), 1)
        q = DataFrameUtil.query_df(self.HGEN_STATE.final_dataset.layer_df,
                                   {LayerKeys.SOURCE_TYPE.value: self.HGEN_ARGS.source_layer_id,
                                    LayerKeys.TARGET_TYPE.value: self.HGEN_ARGS.target_type})
        self.assertEqual(len(q), 1)

    @mock_anthropic
    def test_generate_artifact_content_step_with_clustering(self, anthropic_ai_manager: TestAIManager):
        artifacts, expected_names, n_artifacts_per_cluster, args, state = self._setup_hgen_for_clustering(anthropic_ai_manager,
                                                                                                          generate_trace_links=False)
        GenerateArtifactContentStep().run(args, state)
        RefineGenerationsStep().run(args, state)
        GenerateTraceLinksStep().run(args, state)
        CreateHGenDatasetStep().run(args, state)

        self.assertEqual(len(state.generation_predictions), len(HGenTestConstants.user_stories))
        for i, us in enumerate(state.generation_predictions.keys()):
            self.assertEqual(us, HGenTestConstants.user_stories[i])
            self.assertSetEqual(set(state.generation_predictions[us]),
                                set([a[ArtifactKeys.ID.value] for a in state.id_to_cluster_artifacts[i][:-1]]))

        for cluster_id, cluster_artifacts in state.id_to_cluster_artifacts.items():
            linked_artifact_ids = {art[ArtifactKeys.ID] for i, art in enumerate(cluster_artifacts) if i != n_artifacts_per_cluster - 1}
            new_name = expected_names[cluster_id]
            self.assertIn(new_name, state.final_dataset.artifact_df)
            self.assertNotIn(cluster_id, state.final_dataset.artifact_df)
            for art in artifacts:
                link = state.final_dataset.trace_dataset.trace_df.get_link(source_id=art[ArtifactKeys.ID.value], target_id=new_name)
                self.assertIsNotNone(link)
                if art[ArtifactKeys.ID.value] in linked_artifact_ids:
                    self.assertEqual(link[TraceKeys.SCORE], 0.99)

    @mock_anthropic
    def test_generate_artifact_content_step_with_clustering_and_trace_preds(self, anthropic_ai_manager: TestAIManager):
        artifacts, expected_names, n_artifacts_per_cluster, args, state = self._setup_hgen_for_clustering(anthropic_ai_manager,
                                                                                                          generate_trace_links=True,
                                                                                                          )
        mock_project_summary_responses = MISSING_PROJECT_SUMMARY_RESPONSES
        mock_explanations = [RankingPipelineTest.get_response(task_prompt=SupportedPrompts.EXPLANATION_TASK.value)
                             for _ in range(n_artifacts_per_cluster * len(expected_names))]
        anthropic_ai_manager.add_responses(mock_project_summary_responses + mock_explanations)
        anthropic_ai_manager.mock_summarization()
        GenerateArtifactContentStep().run(args, state)
        RefineGenerationsStep().run(args, state)
        GenerateTraceLinksStep().run(args, state)
        missing = []
        for i, artifact in enumerate(artifacts[:-1]):
            artifact_id = artifact[ArtifactKeys.ID.value]
            cluster_index = math.floor(i / n_artifacts_per_cluster)
            cluster_id = expected_names[cluster_index]
            found = [p for p in state.trace_predictions if p[TraceKeys.child_label()] == artifact_id
                     and p[TraceKeys.parent_label()] == cluster_id]
            if len(found) < 1:
                missing.append((cluster_id, artifact_id))
        self.assertSize(0, missing)

    def _setup_hgen_for_clustering(self, anthropic_ai_manager: TestAIManager,
                                   generate_trace_links: bool = False):

        args: HGenArgs = get_test_hgen_args()()
        args.target_type = "User Story"
        args.generate_trace_links = generate_trace_links
        args.dataset.project_summary = HGEN_PROJECT_SUMMARY
        state = HGenState()
        state.description = HGenTestConstants.description
        state.format_of_artifacts = HGenTestConstants.format_

        state.project_summary = HGEN_PROJECT_SUMMARY
        state.original_dataset = args.dataset
        state.source_dataset = InitializeDatasetStep._create_dataset_with_single_layer(state.original_dataset.artifact_df,
                                                                                       args.source_layer_id)
        artifacts = state.source_dataset.artifact_df.to_artifacts()
        n = 11
        state.id_to_cluster_artifacts = {i: [EnumDict(a) for a in artifacts[i * n:i * n + n]]
                                         for i in range(math.floor(len(artifacts) / n))}
        cluster_dataset = ClusterDatasetCreator(state.source_dataset, manual_clusters={i: [a[ArtifactKeys.ID] for a in artifacts]
                                                                                       for i, artifacts in
                                                                                       state.id_to_cluster_artifacts.items()}) \
            .create()
        state.cluster_dataset = PromptDataset(trace_dataset=cluster_dataset.trace_dataset)
        state.cluster_dataset = PromptDataset(artifact_df=cluster_dataset.artifact_df)
        responses = [PromptUtil.create_xml("user-story", us +
                                           PromptUtil.create_xml("code",
                                                                 ", ".join([a[ArtifactKeys.ID]
                                                                            for a in state.id_to_cluster_artifacts[i][:-1]])))
                     for i, us in enumerate(HGenTestConstants.user_stories)]
        names, expected_names, name_responses = get_name_responses(self.HGEN_STATE.generation_predictions)
        responses.extend(name_responses)
        anthropic_ai_manager.set_responses(responses)
        anthropic_ai_manager.mock_summarization()
        return artifacts, expected_names, n, args, state
