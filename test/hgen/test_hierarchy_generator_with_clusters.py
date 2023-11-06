import math
import random
from copy import deepcopy
from unittest.mock import MagicMock

import mock
import numpy as np

from test.hgen.hgen_test_utils import HGenTestConstants, get_name_responses, get_test_hgen_args, HGEN_PROJECT_SUMMARY, \
    MISSING_PROJECT_SUMMARY_RESPONSES
from test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_trace_links import GenerateTraceLinksStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_name_artifacts import NameArtifactsStep
from tgen.hgen.steps.step_refine_generations import RefineGenerationsStep
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHierarchyGeneratorWithClustering(BaseTest):
    HGEN_ARGS = None
    HGEN_STATE = HGenState()

    @mock_anthropic
    def test_hgen_with_clusters(self, anthropic_ai_manager: TestAIManager):
        artifacts, expected_names, n_artifacts_per_cluster, args, state = self._setup_hgen_for_clustering(anthropic_ai_manager,
                                                                                                          generate_trace_links=True)

        self.assert_generate_artifact_content_step(args, state, anthropic_ai_manager)
        RefineGenerationsStep().run(args, state)
        NameArtifactsStep().run(args, state)
        self.assert_generate_trace_links_step(expected_names, n_artifacts_per_cluster, args, state, anthropic_ai_manager)

    def assert_generate_artifact_content_step(self, args, state,
                                              anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.mock_summarization()
        GenerateArtifactContentStep().run(args, state)
        self.assertEqual(len(state.generation_predictions), len(HGenTestConstants.user_stories))
        for i, us in enumerate(state.generation_predictions.keys()):
            self.assertEqual(us, HGenTestConstants.user_stories[i])
        # TODO test that n_targets is used properly

    @mock.patch.object(EmbeddingUtil, "calculate_similarities")
    def assert_generate_trace_links_step(self, expected_names, n_artifacts_per_cluster, args: HGenArgs, state,
                                         anthropic_ai_manager: TestAIManager,
                                         calculate_sim: MagicMock = None):
        threshold = int(args.link_selection_threshold * 10)
        embedding_similarities = [(random.randint(0, threshold - 1) if i % 2 else random.randint(threshold, 10)) / 10
                                  for i in range(n_artifacts_per_cluster)]
        calculate_sim.return_value = [[np.float32(sim) for sim in embedding_similarities]]
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
                found = [p for p in state.trace_predictions if p[TraceKeys.child_label()] == artifact[ArtifactKeys.ID]
                         and p[TraceKeys.parent_label()] == new_name]
                self.assertEqual(len(found), 1)
                if i % 2 == 0:
                    self.assertIn(TraceKeys.EXPLANATION, found[0])  # assert that this was a selected prediction
                else:
                    self.assertNotIn(TraceKeys.EXPLANATION, found[0])

    def _setup_hgen_for_clustering(self, anthropic_ai_manager: TestAIManager,
                                   generate_trace_links: bool = False):
        args: HGenArgs = get_test_hgen_args()()
        args.target_type = "User Story"
        args.perform_clustering = True
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
        responses = [PromptUtil.create_xml("user-story", us)
                     for i, us in enumerate(HGenTestConstants.user_stories)]
        names, expected_names, name_responses = get_name_responses(self.HGEN_STATE.generation_predictions)
        responses.extend(name_responses)
        anthropic_ai_manager.set_responses(responses)
        anthropic_ai_manager.mock_summarization()
        return artifacts, expected_names, n, args, state
