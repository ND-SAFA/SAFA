from copy import deepcopy
from unittest import mock

from bs4 import BeautifulSoup
from bs4.element import Tag

from tgen_test.hgen.hgen_test_utils import HGEN_PROJECT_SUMMARY, HGenTestConstants, get_name_responses, \
    get_test_hgen_args
from tgen_test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.clustering.base.cluster import Cluster
from tgen.common.constants.deliminator_constants import NEW_LINE, SPACE
from tgen.common.constants.ranking_constants import DEFAULT_TEST_EMBEDDING_MODEL
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.content_generator import ContentGenerator
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_create_clusters import CreateClustersStep
from tgen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from tgen.hgen.steps.step_detect_duplicate_artifacts import DetectDuplicateArtifactsStep
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.hgen.steps.step_generate_explanations_for_links import GenerateExplanationsForLinksStep
from tgen.hgen.steps.step_generate_trace_links import GenerateTraceLinksStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.hgen.steps.step_name_artifacts import NameArtifactsStep
from tgen.hgen.steps.step_refine_generations import RefineGenerationsStep
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHierarchyGeneratorWithClustering(BaseTest):
    HGEN_ARGS: HGenArgs = None

    @mock_anthropic
    def test_hgen_with_clusters(self, anthropic_ai_manager: TestAIManager):
        setup_info = self._setup_hgen_for_clustering(anthropic_ai_manager)
        args, state = setup_info
        CreateClustersStep().run(args, state)
        self.assert_generate_artifact_content_step(args, state, anthropic_ai_manager)

        self.assert_refine_artifact_content_step(args, state, anthropic_ai_manager)
        names, expected_names, name_responses = get_name_responses(state.get_generations2sources().keys())
        anthropic_ai_manager.add_responses(name_responses)
        NameArtifactsStep().run(args, state)
        self.assert_generate_trace_links_step(expected_names, args, state, anthropic_ai_manager)
        self.assert_detect_duplicates_step(args, state)
        self.assert_generate_explanations_step(args, state, anthropic_ai_manager)
        CreateHGenDatasetStep().run(args, state)
        hgen = HierarchyGenerator(self.HGEN_ARGS)
        hgen.state = state
        hgen._log_costs()

    def assert_detect_duplicates_step(self, args, state):
        DUP_SOURCE_ARTIFACT = "dup_link"
        content = state.get_cluster2generation()[list(state.get_cluster2generation().keys())[-1]][0]
        expected_parent = [a_id for a_id, c in state.new_artifact_dataset.artifact_df.to_map().items() if c == content][0]
        dup_artifact_id = "[USD] 4"
        dup_content = NEW_LINE.join([content, "new"])

        state.new_artifact_dataset.artifact_df.add_artifact(dup_artifact_id, dup_content, self.HGEN_ARGS.target_type)
        state.all_artifacts_dataset.artifact_df.add_artifact(dup_artifact_id, dup_content, self.HGEN_ARGS.target_type)

        state.all_artifacts_dataset.artifact_df.add_artifact(DUP_SOURCE_ARTIFACT, content,
                                                             self.HGEN_ARGS.source_layer_ids[0])
        state.source_dataset.artifact_df.add_artifact(DUP_SOURCE_ARTIFACT, content,
                                                      self.HGEN_ARGS.source_layer_ids[0])

        state.embedding_manager.update_or_add_content(DUP_SOURCE_ARTIFACT, content)
        DictUtil.get_value_by_index(state.get_cluster2generation()).append(dup_content)

        original_link = EnumDict({TraceKeys.child_label(): DUP_SOURCE_ARTIFACT,
                                  TraceKeys.parent_label(): dup_artifact_id,
                                  TraceKeys.SCORE: 0.6,
                                  TraceKeys.EXPLANATION: "Explanation"})
        state.selected_predictions.append(deepcopy(original_link))
        DetectDuplicateArtifactsStep().run(args, state)
        self.assertNotIn(dup_artifact_id, state.selected_artifacts_dataset.artifact_df)
        self.assertNotIn(original_link, state.selected_predictions)
        new_link = [trace for trace in state.selected_predictions if trace[TraceKeys.child_label()] == DUP_SOURCE_ARTIFACT]
        self.assertSize(1, new_link)
        self.assertEqual(new_link[0][TraceKeys.TARGET], expected_parent)

    @mock.patch.object(ContentGenerator, "convert_cohesion_to_reduction_percentage", return_value=1)
    def assert_generate_artifact_content_step(self, args, state,
                                              anthropic_ai_manager: TestAIManager, reduction_percentage_mock):

        def prompt_res_creator(r):
            return lambda prompt: self.assert_generation_prompts(prompt, return_value=r)

        user_stories = [HGenTestConstants.user_stories[i % len(HGenTestConstants.user_stories)] + str(i)
                        for i in range(len(state.cluster2artifacts))]
        user_story_res = [PromptUtil.create_xml("user-story", us) for us in user_stories]
        user_story_res[-1] += PromptUtil.create_xml("user-story", user_stories[-1] + str(len(user_story_res)))
        user_stories.append(user_stories[-1] + str(len(user_story_res)))
        responses = [prompt_res_creator(us) for i, us in enumerate(user_story_res)]
        names, expected_names, name_responses = get_name_responses(user_story_res)
        responses.extend(name_responses)
        anthropic_ai_manager.add_responses(responses)
        anthropic_ai_manager.mock_summarization()
        GenerateArtifactContentStep().run(args, state)
        self.assertEqual(len(state.generations2sources), len(state.cluster2artifacts) + 1)
        for i, us in enumerate(state.generations2sources.keys()):
            cluster_id = [c_id for c_id, gen in state.get_cluster2generation().items() if us in gen][0]
            source_artifacts = state.get_cluster2artifacts(ids_only=True)[cluster_id]
            if i < len(state.get_generations2sources()) - 1:
                for a in source_artifacts:
                    self.assertIn(a, us)
            expected_us = user_stories[i]
            self.assertIn(expected_us, us)

    @mock.patch.object(ContentGenerator, "convert_cohesion_to_reduction_percentage", return_value=1)
    def assert_refine_artifact_content_step(self, args, state,
                                            anthropic_ai_manager: TestAIManager, reduction_percentage_mock):
        summary_prompt: Prompt = SupportedPrompts.HGEN_DUP_SUMMARY_TASKS.value
        responses = [PromptUtil.create_xml(summary_prompt.response_manager.response_tag,
                                           f"duplicate summary {i}")
                     for i, _ in enumerate(HGenTestConstants.user_stories)]

        generations2expected_n_targets = {}
        for us in HGenTestConstants.user_stories:
            for gen in state.get_generations2sources():
                if us in gen:
                    if generations2expected_n_targets.get(us, 0) < args.cluster_max_size:
                        DictUtil.set_or_increment_count(generations2expected_n_targets, us)
        for us in HGenTestConstants.user_stories:
            if us in DictUtil.get_value_by_index(state.cluster2generations, index=-1)[0]:
                generations2expected_n_targets[us] -= 1  # intra cluster duplicate

        artifact2n_targets = {a_id: generations2expected_n_targets[[us for us in HGenTestConstants.user_stories
                                                                    if us in state.get_cluster2generation()[c_id][0]][0]]
                              for a_id, c_id in DictUtil.flip(state.cluster2artifacts).items()}

        def prompt_res_creator(r):
            return lambda prompt: self.assert_generation_prompts(prompt, return_value=r, refinement=True,
                                                                 artifact2n_targets=artifact2n_targets)

        user_stories = [PromptUtil.create_xml("user-story", us) for us in HGenTestConstants.user_stories]
        responses.extend([prompt_res_creator(us) for i, us in enumerate(user_stories)])
        anthropic_ai_manager.add_responses(responses)
        RefineGenerationsStep().run(args, state)

    def assert_generate_trace_links_step(self, expected_names,
                                         args: HGenArgs, state,
                                         anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.mock_summarization()
        GenerateTraceLinksStep().run(args, state)
        for i, (cluster_id, cluster_artifacts) in enumerate(state.get_cluster2artifacts().items()):
            new_name = expected_names[i]
            self.assertIn(new_name, state.all_artifacts_dataset.artifact_df)
            self.assertNotIn(cluster_id, state.all_artifacts_dataset.artifact_df)
            for i, artifact in enumerate(cluster_artifacts):
                found_pred = self.find_link(artifact, new_name, state.trace_predictions)
                found_selected = self.find_link(artifact, new_name, state.selected_predictions)
                self.assertEqual(len(found_pred), 1)
                self.assertEqual(len(found_selected), 1)  # assert that this was a selected prediction

    def find_link(self, artifact, new_name, trace_predictions):
        found = [p for p in trace_predictions if p[TraceKeys.child_label()] == artifact[ArtifactKeys.ID]
                 and p[TraceKeys.parent_label()] == new_name]
        return found

    def assert_generation_prompts(self, prompt: str, return_value: str, refinement: bool = False, **kwargs):
        artifacts = BeautifulSoup(prompt, features="lxml").findAll(self.HGEN_ARGS.source_type)
        artifacts = [{ArtifactKeys.ID: child.text
                      for child in a if isinstance(child, Tag) and child.name == "id"}
                     for a in artifacts]
        for a in artifacts:
            a[ArtifactKeys.CONTENT] = self.HGEN_ARGS.dataset.artifact_df.get_artifact(a[ArtifactKeys.ID])[ArtifactKeys.CONTENT]
        source_artifacts = self.HGEN_ARGS.dataset.artifact_df.get_artifacts_by_type(self.HGEN_ARGS.source_layer_ids[0]).to_artifacts()
        avg_file_size = sum([len(a[ArtifactKeys.CONTENT].splitlines())
                             for a in source_artifacts]) / len(source_artifacts)
        if refinement:
            artifact2n_targets = DictUtil.get_kwarg_values(kwargs, artifact2n_targets=None)
            expected_value = artifact2n_targets[artifacts[0][ArtifactKeys.ID]]
        else:
            expected_value = ContentGenerator._calculate_n_targets_for_cluster(artifacts,
                                                                               avg_file_size=avg_file_size,
                                                                               retention_percentage=1)
        self.assertIn("Create {} DISTINCT User Story".format(expected_value), prompt)
        if not refinement:
            end_tag_index = return_value.find(PromptUtil.create_xml_closing("user-story"))
            return_value = return_value[:end_tag_index] + SPACE.join([a[ArtifactKeys.ID] for a in artifacts]) + return_value[
                                                                                                                end_tag_index:]
        return return_value

    def assert_generate_explanations_step(self, args, state, anthropic_ai_manager):
        mock_explanations = [RankingPipelineTest.get_response(task_prompt=SupportedPrompts.EXPLANATION_TASK.value)
                             for _ in state.selected_predictions]
        anthropic_ai_manager.add_responses(mock_explanations)
        GenerateExplanationsForLinksStep().run(args, state)
        missing_explanation = [trace for trace in state.selected_predictions if not trace.get(TraceKeys.EXPLANATION)]
        self.assertEqual(len(missing_explanation), 0)

    def test_n_targets(self):
        artifacts = {"0": "A cat is a furry animal",
                     "1": "Cats are fun to have as pets",
                     "2": "A lion is also a cat",
                     "3": "Have you seen a cat in a hat",
                     "4": "The sky is blue",
                     "5": "Chicago is a city in America",
                     "6": "Veggies are tasty"}
        n_arts_p_cluster = 4
        selected_artifacts = [{str(j * (n_arts_p_cluster - 1) + i) for i in range(n_arts_p_cluster)} for j in range(2)]
        clusters = []
        for i, artifact_set in enumerate(selected_artifacts):
            c = Cluster(embeddings_manager=EmbeddingsManager(artifacts,
                                                             model_name=DEFAULT_TEST_EMBEDDING_MODEL))
            c.add_artifacts(list(artifact_set))
            clusters.append(c)
        art_df = ArtifactDataFrame({ArtifactKeys.ID: list(artifacts.keys()), ArtifactKeys.CONTENT: list(artifacts.values()),
                                    ArtifactKeys.LAYER_ID: ["layer" for _ in artifacts]})
        cluster2artifacts = {str(i): [art_df.get_artifact(a_id) for a_id in cluster.artifact_ids] for i, cluster in
                             enumerate(clusters)}
        cluster2cohesion = {str(i): cluster.avg_pairwise_sim for i, cluster in enumerate(clusters)}
        source_dataset = PromptDataset(artifact_df=art_df)
        n_per_cluster = ContentGenerator.calculate_number_of_targets_per_cluster([str(i) for i in range(len(clusters))],
                                                                                 cluster2artifacts, cluster2cohesion, source_dataset)
        self.assertGreater(n_per_cluster[1], n_per_cluster[0])

    def _setup_hgen_for_clustering(self, anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.mock_summarization()
        args: HGenArgs = get_test_hgen_args(test_refinement=True, test_clustering=True)()
        args.dataset.project_summary = HGEN_PROJECT_SUMMARY
        args.target_type = "User Story"
        self.HGEN_ARGS = args

        hgen = HierarchyGenerator(self.HGEN_ARGS)
        hgen.run_setup_for_pipeline()
        state = hgen.state

        InitializeDatasetStep().run(args, state)

        state.description = HGenTestConstants.description
        state.format_of_artifacts = HGenTestConstants.format_
        state.example_artifact = HGenTestConstants.example
        return args, state
