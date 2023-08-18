import os
from unittest.mock import MagicMock

import mock
import pandas as pd

from test.hgen.hgen_test_utils import get_test_hgen_args, get_name_responses, get_generated_artifacts_response, HGenTestConstants, \
    get_ranking_job_result
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.file_util import FileUtil
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys, ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenState
from tgen.hgen.hgen_util import save_dataset_checkpoint
from tgen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.mocking.mock_anthropic import mock_anthropic
from tgen.testres.testprojects.mocking.mock_libraries import mock_libraries
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestHierarchyGenerator(BaseTest):
    HGEN_ARGS = get_test_hgen_args()
    HGEN_STATE = HGenState()

    def test_run(self):
        self.assert_initialize_dataset_step()
        self.assert_generate_input_step()
        self.assert_generate_artifact_content_step()
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
        safa_save_path = save_dataset_checkpoint(self.HGEN_STATE.dataset, export_path, filename="dir", exporter_class=SafaExporter)
        saved_safa_dataset = TraceDatasetCreator(StructuredProjectReader(project_path=safa_save_path)).create()
        assert_dataset(saved_safa_dataset, self.HGEN_STATE.dataset)
        csv_save_path = save_dataset_checkpoint(self.HGEN_STATE.source_dataset, export_path, filename="artifacts")
        saved_csv_dataset = ArtifactDataFrame(pd.read_csv(csv_save_path))
        self.assertSetEqual(set(saved_csv_dataset.index), set(self.HGEN_STATE.source_dataset.artifact_df.index))
        dataframe_save_path = save_dataset_checkpoint(self.HGEN_STATE.original_dataset, export_path, filename="dir")
        saved_dataframe_dataset = TraceDatasetCreator(DataFrameProjectReader(project_path=dataframe_save_path)).create()
        assert_dataset(saved_dataframe_dataset, self.HGEN_STATE.original_dataset)
        non_dataset = {"hello": "world"}
        yaml_save_path = save_dataset_checkpoint(non_dataset, export_path, filename="non_dataset")
        yaml_content = FileUtil.read_yaml(yaml_save_path)
        self.assertDictEqual(non_dataset, yaml_content)

    def assert_initialize_dataset_step(self):
        orig_dataset = self.HGEN_ARGS.dataset_creator_for_sources.create()
        InitializeDatasetStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assertSetEqual(set(self.HGEN_STATE.original_dataset.artifact_df.index), set(orig_dataset.artifact_df.index))
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
        self.assertEqual(openai_ai_manager.n_used, 1)
        self.assertEqual(anthropic_ai_manager.n_used, 1)
        os.remove(path)

    @mock_anthropic
    def assert_generate_artifact_content_step(self, anthropic_ai_manager: TestAIManager):
        self.HGEN_ARGS.target_type = "User Story"
        response = get_generated_artifacts_response()
        anthropic_ai_manager.set_responses(response)
        step = GenerateArtifactContentStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assertEqual(HGenTestConstants.summary, self.HGEN_STATE.summary)
        for i, us in enumerate(HGenTestConstants.user_stories):
            self.assertEqual(us, self.HGEN_STATE.generated_artifact_content[i])

    @mock_anthropic
    @mock.patch.object(RankingJob, "run")
    def assert_create_dataset_step(self, anthropic_ai_manager: TestAIManager, ranking_mock: MagicMock):
        names, expected_names, responses = get_name_responses(self.HGEN_STATE.generated_artifact_content)
        anthropic_ai_manager.set_responses(responses)
        job_result = get_ranking_job_result(expected_names, self.HGEN_STATE.source_dataset.artifact_df.index)
        ranking_mock.return_value = job_result
        step = CreateHGenDatasetStep()
        step.run(self.HGEN_ARGS, self.HGEN_STATE)
        for id_, link in self.HGEN_STATE.original_dataset.trace_dataset.trace_df.itertuples():
            found_link = self.HGEN_STATE.dataset.trace_df.get_link(source_id=link[TraceKeys.SOURCE], target_id=link[TraceKeys.TARGET])
            self.assertIsNotNone(found_link)
        for name in expected_names:
            self.assertIn(name, self.HGEN_STATE.dataset.artifact_df.index)
            new_artifact = self.HGEN_STATE.dataset.artifact_df.get_artifact(artifact_id=name)
            self.assertEqual(new_artifact[ArtifactKeys.LAYER_ID], self.HGEN_ARGS.target_type)
            for orig_id, orig_artifact in self.HGEN_STATE.original_dataset.artifact_df.itertuples():
                self.assertIn(orig_id, self.HGEN_STATE.dataset.artifact_df.index)
                if orig_artifact[ArtifactKeys.LAYER_ID] == self.HGEN_ARGS.source_layer_id:
                    q = DataFrameUtil.query_df(self.HGEN_STATE.dataset.trace_df, {"source": orig_id, "target": name})
                    self.assertEqual(len(q), 1)
        for i, layer in self.HGEN_STATE.original_dataset.trace_dataset.layer_df.itertuples():
            q = DataFrameUtil.query_df(self.HGEN_STATE.dataset.layer_df, layer)
            self.assertEqual(len(q), 1)
        q = DataFrameUtil.query_df(self.HGEN_STATE.dataset.layer_df, {LayerKeys.SOURCE_TYPE.value: self.HGEN_ARGS.source_layer_id,
                                                                      LayerKeys.TARGET_TYPE.value: self.HGEN_ARGS.target_type})
        self.assertEqual(len(q), 1)
