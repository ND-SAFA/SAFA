import math
from unittest import mock
from unittest.mock import MagicMock

from tgen_test.hgen.hgen_test_utils import HGenTestConstants, get_all_responses, get_predictions
from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.project_summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.status import Status
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob
from tgen.summarizer.summary import Summary
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_libraries import mock_libraries
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.paths.paths import TEST_HGEN_PATH
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep


class TestMultiLayerHGenJob(BaseJobTest):
    higher_levels = ["requirement", "design document"]
    ranking_calls = 0
    clustering_calls = 0

    def fake_ranking_job_run(self, expected_names, source_artifact_names):
        expected_name = expected_names[self.ranking_calls]
        source_artifact_name = source_artifact_names[self.ranking_calls]
        self.ranking_calls += 1
        return get_predictions(expected_name, source_artifact_name)

    @mock_libraries
    @mock.patch.object(AddClustersToDataset, "run")
    @mock.patch.object(CompleteRankingPromptsStep, "complete_ranking_prompts")
    def test_run_success(self, anthropic_ai_manager: TestAIManager, openai_ai_manager: TestAIManager,
                         ranking_mock: MagicMock, final_cluster_step: MagicMock):
        """
        Tests that job is completed succesfully.
        """
        self.ranking_calls = 0
        self.clustering_calls = 0
        args: HGenArgs = self.get_args()
        args.run_refinement = False
        source_arts = args.dataset.artifact_df.filter_by_row(lambda row:
                                                             row[ArtifactKeys.LAYER_ID.value]
                                                             ==
                                                             args.source_layer_ids)
        final_cluster_step.side_effect = self.set_clustering_state

        expected_user_story_names, anthropic_responses = get_all_responses(target_type=args.target_type)

        requirements = ["This is a requirement for a user story.", "This is another requirement for some user stories."]
        design_document = ["Here is the final, top level design document"]
        expected_requirements_names, responses = get_all_responses(content=requirements, target_type=self.higher_levels[0],
                                                                   source_type=args.target_type,
                                                                   sources=[expected_user_story_names[:2],
                                                                            [expected_user_story_names[-1]]])
        anthropic_responses.extend(responses)
        expected_design_doc_name, responses = get_all_responses(content=design_document, target_type=self.higher_levels[1],
                                                                source_type=self.higher_levels[0],
                                                                sources=[[expected_requirements_names[0]],
                                                                         [expected_requirements_names[1]]])
        anthropic_responses.extend(responses)

        anthropic_ai_manager.mock_summarization()
        anthropic_ai_manager.set_responses(anthropic_responses)
        open_ai_responses = HGenTestConstants.open_ai_responses * 3
        openai_ai_manager.set_responses(open_ai_responses)
        ranking_mock.side_effect = lambda _, __: self.fake_ranking_job_run([expected_user_story_names,
                                                                            expected_requirements_names,
                                                                            expected_design_doc_name],
                                                                           [source_arts.index, expected_user_story_names,
                                                                            expected_requirements_names])

        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        self.assertEqual(job_result.status, Status.SUCCESS)
        args = self.get_args()
        target_types = [args.target_type] + self.higher_levels
        source_types = [args.source_type, args.target_type, self.higher_levels[0]]
        for target, source in zip(target_types, source_types):
            FileUtil.delete_file_safely(GenerateInputsStep._get_inputs_save_path(target, source))
        orig_dataset = args.dataset_creator.create()
        self.assertEqual(job_result.status, Status.SUCCESS)
        dataset: TraceDataset = job_result.body
        if isinstance(dataset, str):
            self.fail(dataset)
        orig_layers = set(orig_dataset.artifact_df[ArtifactKeys.LAYER_ID])
        layers = args.source_layer_ids + [args.target_type, self.higher_levels[0], self.higher_levels[1]]
        n_expected_links = 0
        for i, layer in enumerate(layers):
            target_artifacts = dataset.artifact_df.get_artifacts_by_type(layer)
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
                matching_layers = dataset.layer_df.get_layer(layer, layers[i + 1])
                self.assertGreaterEqual(len(matching_layers), 1)
        # todo: original trace links are added to exported data frame as per hgen arg.
        # self.assertEqual(n_expected_links + len(orig_dataset.trace_dataset.trace_df), len(dataset.trace_df))

    @mock_anthropic
    def get_args(self, anthropic_ai_manager: TestAIManager, **kwargs):
        anthropic_ai_manager.mock_summarization()
        project_summary_sections = {sec for sec in HierarchyGenerator.PROJECT_SUMMARY_SECTIONS}
        project_summary_sections.update(set(DEFAULT_PROJECT_SUMMARY_SECTIONS))
        args = HGenArgs(source_layer_ids="C++ Code",
                        target_type="Test User Story",
                        dataset_creator=PromptDatasetCreator(
                            project_summary=Summary({title: EnumDict({"title": title, "chunks": ["summary of project"]})
                                                     for title in project_summary_sections}),
                            trace_dataset_creator=TraceDatasetCreator(DataFrameProjectReader(project_path=TEST_HGEN_PATH))),
                        create_new_code_summaries=False, **kwargs)
        return args

    def _get_job(self):
        args: HGenArgs = self.get_args(export_dir=EMPTY_STRING)
        args.generate_explanations = False
        args.run_refinement = False
        starting_hgen_job = BaseHGenJob(args)
        return MultiLayerHGenJob(starting_hgen_job, self.higher_levels)

    def set_clustering_state(self, args: ClusteringArgs, state: ClusteringState, *other_args, **other_kwargs):
        artifacts = args.dataset.artifact_df.to_artifacts()
        divisor = 3 - self.clustering_calls
        n = math.floor(len(artifacts) / divisor)
        state.final_cluster_map = {
            str(i): Cluster.from_artifacts([a[ArtifactKeys.ID.value] for a in artifacts[i * n:i * n + n]], state.embedding_manager) for
            i in
            range(divisor)}
        cluster_dataset = ClusterDatasetCreator(args.dataset, state.final_cluster_map).create()
        state.cluster_dataset = PromptDataset(trace_dataset=cluster_dataset.trace_dataset)
        state.cluster_artifact_dataset = PromptDataset(artifact_df=cluster_dataset.artifact_df)

        self.clustering_calls += 1
