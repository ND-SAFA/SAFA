from unittest import mock
from unittest.mock import MagicMock

from test.hgen.hgen_test_utils import HGenTestConstants, get_all_responses, get_ranking_job_result
from tgen.common.util.file_util import FileUtil
from tgen.common.util.status import Status
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerKeys
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.paths.paths import TEST_HGEN_PATH
from tgen.testres.mocking.mock_libraries import mock_libraries
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestMultiLayerHGenJob(BaseJobTest):
    args = HGenArgs(source_layer_id="C++ Code",
                    target_type="Test User Story",
                    dataset_creator_for_sources=PromptDatasetCreator(
                        trace_dataset_creator=TraceDatasetCreator(DataFrameProjectReader(project_path=TEST_HGEN_PATH))),
                    create_new_code_summaries=False,)
    higher_levels = ["requirement", "design document"]
    ranking_calls = 0

    def fake_ranking_job_run(self, expected_names, source_artifact_names):
        expected_name = expected_names[self.ranking_calls]
        source_artifact_name = source_artifact_names[self.ranking_calls]
        self.ranking_calls += 1
        return get_ranking_job_result(expected_name, source_artifact_name)

    @mock_libraries
    @mock.patch.object(RankingJob, "run")
    def test_run_success(self, anthropic_ai_manager: TestAIManager, openai_ai_manager: TestAIManager, ranking_mock: MagicMock):
        """
        Tests that job is completed succesfully.
        """
        source_arts = self.args.dataset_creator_for_sources.create().artifact_df.filter_by_row(lambda row:
                                                                                               row[ArtifactKeys.LAYER_ID.value]
                                                                                               ==
                                                                                               self.args.source_layer_id)
        self.ranking_calls = 0
        expected_user_story_names, anthropic_responses = get_all_responses(target_type=self.args.target_type)

        requirements = ["This is a requirement for a user story.", "This is another requirement for some user stories."]
        design_document = ["Here is the final, top level design document"]
        expected_requirements_names, responses = get_all_responses(content=requirements, target_type=self.higher_levels[0])
        anthropic_responses.extend(responses)
        expected_design_doc_name, responses = get_all_responses(content=design_document, target_type=self.higher_levels[1])
        anthropic_responses.extend(responses)

        anthropic_ai_manager.set_responses(anthropic_responses)
        open_ai_responses = HGenTestConstants.open_ai_responses * 3
        openai_ai_manager.set_responses(open_ai_responses)
        ranking_mock.side_effect = lambda: self.fake_ranking_job_run([expected_user_story_names,
                                                                      expected_requirements_names,
                                                                      expected_design_doc_name],
                                                                     [source_arts.index, expected_user_story_names,
                                                                      expected_requirements_names])

        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        self.assertEqual(job_result.status, Status.SUCCESS)
        target_types = [self.args.target_type] + self.higher_levels
        source_types = [self.args.source_type, self.args.target_type, self.higher_levels[0]]
        for target, source in zip(target_types, source_types):
            FileUtil.delete_file_safely(GenerateInputsStep._get_inputs_save_path(target, source))
        orig_dataset = self.args.dataset_creator_for_sources.create()
        dataset: TraceDataset = job_result.body
        orig_layers = set(orig_dataset.artifact_df[ArtifactKeys.LAYER_ID])
        layers = [self.args.source_layer_id] + [self.args.target_type, self.higher_levels[0],
                                                self.higher_levels[1]]
        n_expected_links = 0
        for i, layer in enumerate(layers):
            target_artifacts = dataset.artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layer)
            if layer in orig_layers:
                n_source_artifacts = orig_dataset.artifact_df.get_type_counts()[layer]
                self.assertSize(n_source_artifacts, target_artifacts)
            else:
                self.assertGreater(len(target_artifacts), 0)
                as_target = dataset.layer_df.filter_by_row(lambda row: row[LayerKeys.TARGET_TYPE.value] == layer
                                                                       and row[LayerKeys.SOURCE_TYPE.value] == layers[i - 1])
                source_artifacts = dataset.artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layers[i - 1])
                self.assertGreater(len(as_target), 0)
                n_expected_links += len(target_artifacts) * len(source_artifacts)
            if layer != layers[len(layers) - 1]:
                as_source = dataset.layer_df.filter_by_row(lambda row: row[LayerKeys.SOURCE_TYPE.value] == layer
                                                                       and row[LayerKeys.TARGET_TYPE.value] == layers[i + 1])
                self.assertGreater(len(as_source), 0)
        self.assertEqual(n_expected_links + len(orig_dataset.trace_dataset.trace_df), len(dataset.trace_df))

    def _get_job(self):
        starting_hgen_job = BaseHGenJob(self.args)
        return MultiLayerHGenJob(starting_hgen_job, self.higher_levels)
