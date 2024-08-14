import os
from unittest.mock import MagicMock

import mock
import numpy as np
import pandas as pd
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.exporters.safa_exporter import SafaExporter
from common_resources.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys
from common_resources.data.readers.dataframe_project_reader import DataFrameProjectReader
from common_resources.data.readers.structured_project_reader import StructuredProjectReader
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.mock_libraries import mock_libraries
from common_resources.mocking.test_response_manager import TestAIManager
from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.file_util import FileUtil

from tgen.common.util.pipeline_util import PipelineUtil
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_create_clusters import CreateClustersStep
from tgen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_detect_duplicate_artifacts import DetectDuplicateArtifactsStep
from tgen.hgen.steps.step_find_homes_for_orphans import FindHomesForOrphansStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_explanations_for_links import GenerateExplanationsForLinksStep
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.hgen.steps.step_generate_trace_links import GenerateTraceLinksStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_name_artifacts import NameArtifactsStep
from tgen.hgen.steps.step_refine_generations import RefineGenerationsStep
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen_test.hgen.hgen_test_utils import HGenTestConstants, get_generated_artifacts_response, get_name_responses, get_test_hgen_args
from tgen_test.ranking.steps.ranking_pipeline_test import RankingPipelineTest


class TestHierarchyGenerator(BaseTest):
    HGEN_ARGS = None
    HGEN_STATE = None

    @mock_anthropic
    def test_run(self, anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.require_used_all_responses = False  # TODO: Investigate why too many link explanations responses.
        anthropic_ai_manager.mock_summarization()
        self.HGEN_ARGS = get_test_hgen_args(test_refinement=True)()
        self.HGEN_ARGS.perform_clustering = False
        self.HGEN_ARGS.duplicate_similarity_threshold = 0.65
        hgen = HierarchyGenerator(self.HGEN_ARGS)
        hgen.run_setup_for_pipeline()
        self.HGEN_STATE = hgen.state
        self.assert_initialize_dataset_step()
        self.assert_generate_input_step()
        CreateClustersStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assert_generate_artifact_content_step(anthropic_ai_manager=anthropic_ai_manager)
        RefineGenerationsStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assert_name_artifacts_step(anthropic_ai_manager=anthropic_ai_manager)
        self.assert_generate_trace_links_step(anthropic_ai_manager=anthropic_ai_manager)
        DetectDuplicateArtifactsStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assert_find_homes_for_orphans_step()
        self.assert_generate_explanations_for_links_step(anthropic_ai_manager=anthropic_ai_manager)
        self.assert_create_dataset_step()
        self.assert_save_dataset_checkpoint()
        hgen._log_costs()

    def assert_save_dataset_checkpoint(self):
        def assert_dataset(dataset: TraceDataset, orig_dataset: TraceDataset, msg: str = None):
            self.assertSetEqual(set(dataset.artifact_df.index), set(orig_dataset.artifact_df.index), msg=msg)
            self.assertEqual(len(dataset.trace_df), len(orig_dataset.trace_df), msg=msg)
            for i, trace in orig_dataset.trace_df.itertuples():
                self.assertIsNotNone(dataset.trace_df.get_link(source_id=trace[TraceKeys.SOURCE], target_id=trace[TraceKeys.TARGET]),
                                     msg=msg)
            self.assertEqual(len(dataset.layer_df), len(orig_dataset.layer_df), msg=msg)

        export_path = TEST_OUTPUT_DIR
        artifact_df = self.HGEN_STATE.final_dataset.trace_dataset.artifact_df
        self.HGEN_STATE.final_dataset.update_artifact_df(artifact_df)
        safa_save_path = PipelineUtil.save_dataset_checkpoint(self.HGEN_STATE.final_dataset, export_path, filename="dir",
                                                              exporter_class=SafaExporter)
        saved_safa_dataset = TraceDatasetCreator(StructuredProjectReader(project_path=safa_save_path)).create()
        assert_dataset(saved_safa_dataset, self.HGEN_STATE.final_dataset, msg="Exported does not match final dataset.")
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

    def assert_generate_artifact_content_step(self, anthropic_ai_manager: TestAIManager):
        self.HGEN_ARGS.target_type = "User Story"
        response = get_generated_artifacts_response()
        anthropic_ai_manager.add_responses(response)
        step = GenerateArtifactContentStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for i, us in enumerate(self.HGEN_STATE.generations2sources.keys()):
            self.assertEqual(us, HGenTestConstants.user_stories[i])
            self.assertEqual(set(self.HGEN_STATE.generations2sources[us]), set(HGenTestConstants.code_files[i]))

    def assert_name_artifacts_step(self, anthropic_ai_manager: TestAIManager):
        names, expected_names, name_responses = get_name_responses(self.HGEN_STATE.get_generations2sources())
        anthropic_ai_manager.add_responses(name_responses)
        NameArtifactsStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        for name in expected_names:
            self.assertIn(name, list(self.HGEN_STATE.all_artifacts_dataset.artifact_df.index))

    @mock.patch.object(EmbeddingsManager, "compare_artifacts")
    def assert_generate_trace_links_step(self, sim_mock: MagicMock, anthropic_ai_manager: TestAIManager, ):
        responses = []
        embedding_similarities = [0.8 for source in self.HGEN_STATE.source_dataset.artifact_df.index]
        new_artifact_names = list(self.HGEN_STATE.new_artifact_dataset.artifact_df.index)
        responses.extend([RankingPipelineTest.get_response(task_prompt=SupportedPrompts.EXPLANATION_TASK.value)
                          for _ in embedding_similarities] * len(new_artifact_names))
        anthropic_ai_manager.add_responses(responses)
        anthropic_ai_manager.mock_summarization()

        sim_mock.return_value = np.array(
            [np.array([np.float32(sim) for sim in embedding_similarities]) for i in new_artifact_names])
        step = GenerateTraceLinksStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)

        us2code = {us: code for us, code in zip(new_artifact_names, HGenTestConstants.code_files)}
        for new_pred in self.HGEN_STATE.trace_predictions:
            parent = new_pred[TraceKeys.parent_label()]
            child = new_pred[TraceKeys.child_label()]
            if child in us2code[parent]:
                self.assertGreater(new_pred[TraceKeys.SCORE], 0.8)  # these should be weighted higher than original prediction

    def assert_generate_explanations_for_links_step(self, anthropic_ai_manager):
        GenerateExplanationsForLinksStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        missing_explanation = [trace for trace in self.HGEN_STATE.selected_predictions if not trace.get(TraceKeys.EXPLANATION)]
        self.assertEqual(len(missing_explanation), 0)

    def assert_create_dataset_step(self):
        step = CreateHGenDatasetStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for id_, link in self.HGEN_STATE.original_dataset.trace_dataset.trace_df.itertuples():
            found_link = self.HGEN_STATE.final_dataset.trace_df.get_link(source_id=link[TraceKeys.SOURCE],
                                                                         target_id=link[TraceKeys.TARGET])
            self.assertIsNotNone(found_link)
        for content in self.HGEN_STATE.get_generations2sources().keys():
            found_artifact = self.HGEN_STATE.final_dataset.artifact_df.filter_by_row(lambda row:
                                                                                     row[ArtifactKeys.CONTENT.value] == content
                                                                                     and row[
                                                                                         ArtifactKeys.LAYER_ID.value] == self.HGEN_ARGS.target_type)
            self.assertEqual(len(found_artifact), 1)
            name = found_artifact.index[0]
            new_artifact = self.HGEN_STATE.final_dataset.artifact_df.get_artifact(name)
            self.assertEqual(new_artifact[ArtifactKeys.LAYER_ID], self.HGEN_ARGS.target_type)
            for orig_id, orig_artifact in self.HGEN_STATE.original_dataset.artifact_df.itertuples():
                self.assertIn(orig_id, self.HGEN_STATE.final_dataset.artifact_df.index)

                if orig_id in self.HGEN_ARGS.source_layer_ids:
                    q = DataFrameUtil.query_df(self.HGEN_STATE.final_dataset.trace_df, {"source": orig_id, "target": name})
                    self.assertEqual(len(q), 1)
        for i, layer in self.HGEN_STATE.original_dataset.trace_dataset.layer_df.itertuples():
            q = DataFrameUtil.query_df(self.HGEN_STATE.final_dataset.layer_df, layer)
            self.assertEqual(len(q), 1)
        q = DataFrameUtil.query_df(self.HGEN_STATE.final_dataset.layer_df,
                                   {LayerKeys.SOURCE_TYPE.value: self.HGEN_ARGS.source_layer_ids[0],
                                    LayerKeys.TARGET_TYPE.value: self.HGEN_ARGS.target_type})
        self.assertEqual(len(q), 1)

    def assert_find_homes_for_orphans_step(self):
        FindHomesForOrphansStep().run(self.HGEN_ARGS, self.HGEN_STATE)
