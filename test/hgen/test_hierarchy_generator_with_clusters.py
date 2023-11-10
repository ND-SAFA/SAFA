import math
import random
from copy import deepcopy
from unittest.mock import MagicMock

import mock
import numpy as np
from bs4 import BeautifulSoup

from test.hgen.hgen_test_utils import HGEN_PROJECT_SUMMARY, HGenTestConstants, MISSING_PROJECT_SUMMARY_RESPONSES, get_name_responses, \
    get_test_hgen_args
from test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.common.constants.hgen_constants import DEFAULT_BRANCHING_FACTOR
from tgen.common.constants.project_summary_constants import PS_ENTITIES_TITLE
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_create_clusters import CreateClustersStep
from tgen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_detect_duplicate_artifacts import DetectDuplicateArtifactsStep
from tgen.hgen.steps.step_find_homes_for_orphans import FindHomesForOrphansStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_explanations_for_links import GenerateExplanationsForLinksStep
from tgen.hgen.steps.step_generate_trace_links import GenerateTraceLinksStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_name_artifacts import NameArtifactsStep
from tgen.hgen.steps.step_refine_generations import RefineGenerationsStep
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHierarchyGeneratorWithClustering(BaseTest):
    HGEN_ARGS: HGenArgs = None

    @mock_anthropic
    def test_hgen_with_clusters(self, anthropic_ai_manager: TestAIManager):
        expected_names, args, state = self._setup_hgen_for_clustering(anthropic_ai_manager, generate_trace_links=True)
        CreateClustersStep().run(args, state)
        artifacts, n_artifacts_per_cluster, n_artifacts_last_cluster = self._setup_state_post_clustering_step(state)
        self.assert_generate_artifact_content_step(args, state, anthropic_ai_manager)

        self._reset_cluster_artifacts_for_tracing_test(n_artifacts_last_cluster, n_artifacts_per_cluster, state)

        RefineGenerationsStep().run(args, state)
        NameArtifactsStep().run(args, state)
        self.assert_generate_trace_links_step(expected_names, n_artifacts_per_cluster,
                                              args, state, anthropic_ai_manager)
        DetectDuplicateArtifactsStep().run(args, state)
        self.assert_find_homes_for_orphans(args, state, len(artifacts), anthropic_ai_manager)
        self.assert_generate_explanations_step(args, state)
        CreateHGenDatasetStep().run(args, state)
        hgen = HierarchyGenerator(self.HGEN_ARGS)
        hgen.state = state
        hgen._log_costs()

    def assert_generate_artifact_content_step(self, args, state,
                                              anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.mock_summarization()
        GenerateArtifactContentStep().run(args, state)
        self.assertEqual(len(state.generation_predictions), len(HGenTestConstants.user_stories))
        for i, us in enumerate(state.generation_predictions.keys()):
            self.assertEqual(us, HGenTestConstants.user_stories[i])

    @mock.patch.object(EmbeddingUtil, "calculate_similarities")
    def assert_generate_trace_links_step(self, expected_names, n_artifacts_per_cluster,
                                         args: HGenArgs, state,
                                         anthropic_ai_manager: TestAIManager,
                                         calculate_sim: MagicMock = None):
        embedding_similarities = self._create_fake_embedding_scores(args, calculate_sim, n_artifacts_per_cluster)
        mock_project_summary_responses = deepcopy(MISSING_PROJECT_SUMMARY_RESPONSES)

        mock_explanations = [RankingPipelineTest.get_response(task_prompt=SupportedPrompts.EXPLANATION_TASK.value)
                             for sim in embedding_similarities if sim >= args.link_selection_threshold] * len(expected_names)
        anthropic_ai_manager.add_responses(mock_project_summary_responses + mock_explanations)
        anthropic_ai_manager.mock_summarization()
        GenerateTraceLinksStep().run(args, state)
        for cluster_id, cluster_artifacts in state.id_to_cluster_artifacts.items():
            new_name = expected_names[cluster_id]
            self.assertIn(new_name, state.all_artifacts_dataset.artifact_df)
            self.assertNotIn(cluster_id, state.all_artifacts_dataset.artifact_df)
            for i, artifact in enumerate(cluster_artifacts):
                found_pred = self.find_link(artifact, new_name, state.trace_predictions)
                found_selected = self.find_link(artifact, new_name, state.selected_predictions)
                self.assertEqual(len(found_pred), 1)
                if i % 2 == 0:
                    self.assertEqual(len(found_selected), 1)  # assert that this was a selected prediction
                else:
                    self.assertEqual(len(found_selected), 0)

    def find_link(self, artifact, new_name, trace_predictions):
        found = [p for p in trace_predictions if p[TraceKeys.child_label()] == artifact[ArtifactKeys.ID]
                 and p[TraceKeys.parent_label()] == new_name]
        return found

    def assert_generation_prompts(self, prompt: str, return_value: str):
        n_artifacts = len(BeautifulSoup(prompt, features="lxml").findAll(self.HGEN_ARGS.source_type))
        expected_value = GenerateArtifactContentStep._calculate_proportion_of_artifacts(n_artifacts, DEFAULT_BRANCHING_FACTOR)
        self.assertIn(f"a minimal set ({expected_value})", prompt)
        return return_value

    @mock.patch.object(EmbeddingUtil, "calculate_similarities")
    def assert_find_homes_for_orphans(self, args: HGenArgs, state: HGenState, n_artifacts, anthropic_manager, sim_mock: MagicMock):
        selected_sources = {trace[TraceKeys.SOURCE] for trace in state.selected_predictions}
        n_added_sources = len({trace[TraceKeys.SOURCE] for trace in state.trace_predictions
                               if trace[TraceKeys.SCORE] >= args.min_orphan_score_threshold}) - len(selected_sources)
        n_added_sources = max(n_added_sources, 0)
        n_orphans = n_artifacts - len(selected_sources) - n_added_sources
        embedding_similarities = self._create_fake_embedding_scores(args, sim_mock, n_orphans)
        n_explanations = n_added_sources + len([s for s in embedding_similarities if s >= args.min_orphan_score_threshold])
        anthropic_manager.add_responses([RankingPipelineTest.get_response(task_prompt=SupportedPrompts.EXPLANATION_TASK.value)
                                         for _ in range(n_explanations)])
        FindHomesForOrphansStep().run(args, state)

    def assert_generate_explanations_step(self, args, state):
        GenerateExplanationsForLinksStep().run(args, state)
        missing_explanation = [trace for trace in state.selected_predictions if not trace.get(TraceKeys.EXPLANATION)]
        self.assertEqual(len(missing_explanation), 0)

    def _create_fake_embedding_scores(self, args, calculate_sim_mock, n_artifacts):
        threshold = int(args.link_selection_threshold * 10)
        embedding_similarities = [(random.randint(0, threshold - 1) if i % 2 else random.randint(threshold, 10)) / 10
                                  for i in range(n_artifacts)]
        calculate_sim_mock.return_value = [[np.float32(sim) for sim in embedding_similarities]]
        return embedding_similarities

    def _setup_hgen_for_clustering(self, anthropic_ai_manager: TestAIManager,
                                   generate_trace_links: bool = False):
        def prompt_res_creator(r):
            return lambda prompt: self.assert_generation_prompts(prompt, return_value=r)

        anthropic_ai_manager.mock_summarization()
        anthropic_ai_manager.set_responses([MockResponses.project_title_to_response[PS_ENTITIES_TITLE]])
        args: HGenArgs = get_test_hgen_args()()
        self.HGEN_ARGS = args
        args.target_type = "User Story"
        args.perform_clustering = True
        args.generate_trace_links = generate_trace_links
        hgen = HierarchyGenerator(self.HGEN_ARGS)
        hgen.run_setup_for_pipeline()
        state = hgen.state
        state.description = HGenTestConstants.description
        state.format_of_artifacts = HGenTestConstants.format_

        state.project_summary = HGEN_PROJECT_SUMMARY
        state.original_dataset = args.dataset
        state.source_dataset = InitializeDatasetStep._create_dataset_with_single_layer(state.original_dataset.artifact_df,
                                                                                       args.source_layer_id)

        user_story_responses = [PromptUtil.create_xml("user-story", us) for i, us in enumerate(HGenTestConstants.user_stories)]

        responses = [prompt_res_creator(user_story_responses[i]) for i in range(len(user_story_responses))]
        names, expected_names, name_responses = get_name_responses(state.generation_predictions)
        responses.extend(name_responses)
        anthropic_ai_manager.add_responses(responses)
        anthropic_ai_manager.mock_summarization()
        return expected_names, args, state

    def _reset_cluster_artifacts_for_tracing_test(self, n_artifacts_last_cluster, n_artifacts_per_cluster, state):
        # makes it easier to test tracing
        added_artifacts_to_last_cluster = n_artifacts_last_cluster - n_artifacts_per_cluster
        last_cluster_artifacts = state.id_to_cluster_artifacts[len(state.generation_predictions) - 1]
        state.id_to_cluster_artifacts[len(state.generation_predictions) - 1] = last_cluster_artifacts[
                                                                               :-added_artifacts_to_last_cluster]

    def _setup_state_post_clustering_step(self, state):
        # makes it easier to test tracing + generation
        artifacts = state.source_dataset.artifact_df.to_artifacts()
        n = 11
        n_artifacts_last_cluster = n
        n_clusters = math.floor(len(artifacts) / n)
        state.id_to_cluster_artifacts = {i: [EnumDict(a) for a in artifacts[i * n:i * n + n]]
                                         for i in range(n_clusters)}
        if n_clusters * n < len(artifacts):
            rem = n_clusters * n
            added_clusters = [EnumDict(a) for a in artifacts[rem:] + artifacts[:2]]
            state.id_to_cluster_artifacts[n_clusters - 1].extend(added_clusters)
            n_artifacts_last_cluster += len(added_clusters)

        manual_clusters = {i: [a[ArtifactKeys.ID] for a in artifacts] for i, artifacts in state.id_to_cluster_artifacts.items()}
        cluster_dataset = ClusterDatasetCreator(state.source_dataset, manual_clusters).create()
        state.cluster_dataset = PromptDataset(artifact_df=cluster_dataset.artifact_df)
        return artifacts, n, n_artifacts_last_cluster,
