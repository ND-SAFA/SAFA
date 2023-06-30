import os
import uuid
from copy import deepcopy
from unittest import mock

from tgen.data.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.state.llm_trainer_state import LLMTrainerState
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.test_anthropic_responses import fake_anthropic_completion
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.testres.testprojects.prompt_test_project import PromptTestProject
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.util.enum_util import EnumDict
from tgen.util.llm_response_util import LLMResponseUtil


def fake_clustering(artifact_df: TraceDataset, cluster_method: SupportedClusteringMethod, **kwargs):
    artifact_to_cluster = {node: str(i % 4) for i, node in enumerate(list(artifact_df.index))}
    clusters = {}
    for artifact_id, cluster_num in artifact_to_cluster.items():
        if cluster_num not in clusters:
            clusters[cluster_num] = []
        clusters[cluster_num].append(artifact_id)
    return {cluster_method: {uuid.uuid4(): artifacts for cluster_num, artifacts in clusters.items()}}


class TestHierarchyGeneration(BaseTest):
    LAYER_ID = str(uuid.uuid4())
    TARGET_TYPE = "user_story"
    FAKE_CLASSIFICATION_OUTPUT = {
        "classification": "A",
        "justification": "Something",
        "source_subsystem": "source_subsystem",
        "target_subsystem": "target_subsystem",
        "similarity": "0.8",
        "difference": "difference",
        "score": "0.9",
    }

    class FakeDatasetCreator:

        def create(self) -> TraceDataset:
            trace_dataset_creator = TestHierarchyGeneration.get_dataset_creator_with_trace_dataset_creator()
            trainer_dataset_manager = TestHierarchyGeneration.get_trainer_dataset_manager(trace_dataset_creator)
            return trainer_dataset_manager[DatasetRole.EVAL]

    @mock.patch.object(ClusterDatasetCreator, "get_clusters")
    @mock.patch.object(AnthropicManager, "make_completion_request_impl", side_effect=fake_anthropic_completion)
    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    @mock.patch.object(LLMResponseUtil, "extract_labels")
    def test_run(self, llm_response_mock: mock.MagicMock, mock_completion_open_ai: mock.MagicMock,
                 mock_completion_anthr: mock.MagicMock, mock_cluster: mock.MagicMock):
        llm_response_mock.return_value = self.FAKE_CLASSIFICATION_OUTPUT

        dataset_creators = [self.get_dataset_creator_with_artifact_project_reader(),
                            self.get_dataset_creator_with_trace_dataset_creator(),
                            self.FakeDatasetCreator()]
        for i, dataset_creator in enumerate(dataset_creators):
            tgen_trainer = self.get_tgen_trainer(dataset_creator) if not isinstance(dataset_creator, self.FakeDatasetCreator) else None
            hgen = self.get_hierarchy_generator(tgen_trainer=tgen_trainer, dataset_creator_for_sources=dataset_creator)
            orig_dataset = tgen_trainer.trainer_dataset_manager[DatasetRole.EVAL] if tgen_trainer is not None \
                else PromptDataset(trace_dataset=dataset_creator.create())
            mock_cluster.side_effect = lambda: fake_clustering(artifact_df=orig_dataset.artifact_df,
                                                               cluster_method=hgen.args.clustering_method)
            generated_dataset = hgen.run()
            self.assertEqual(len(orig_dataset.artifact_df) + 4, len(generated_dataset.artifact_df))
            expected_n_traces = len(orig_dataset.artifact_df) * 4
            self.assertEqual(expected_n_traces, len(generated_dataset))
            expected_n_layers = 1
            self.assertEqual(expected_n_layers, len(generated_dataset.layer_df))

    def test_create_artifacts_df_with_generated_artifacts(self):
        hgen_dataset = PromptTestProject.get_trace_dataset_creator().create()
        generated_content = "generated content"
        tag = HierarchyGenerator.GENERATION_TAG
        artifact_generations = [f"<{tag}>{generated_content}</{tag}>" for _ in hgen_dataset.artifact_df.index]
        orig_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ["original_id"], ArtifactKeys.CONTENT: ["original_content"],
                                              ArtifactKeys.LAYER_ID: ["original_layer"]})
        artifact_df = HierarchyGenerator._create_artifact_df_with_generated_artifacts(artifact_generations, hgen_dataset.artifact_df,
                                                                                      orig_artifact_df)
        expected_entities = [EnumDict({ArtifactKeys.ID: id_, ArtifactKeys.CONTENT: artifact[ArtifactKeys.CONTENT]})
                             for id_, artifact in orig_artifact_df.itertuples()]
        expected_entities.extend([EnumDict({ArtifactKeys.ID: id_, ArtifactKeys.CONTENT: generated_content})
                                  for id_ in hgen_dataset.artifact_df.index])
        TestAssertions.verify_entities_in_df(self, expected_entities, artifact_df)

    def test_create_trace_df_with_generated_artifacts(self):
        def verify_trace_df(df, n_expected):
            self.assertEqual(len(trace_df), n_expected)
            for source_id, artifact in layer_artifacts.itertuples():
                for target_id in range(n_clusters):
                    self.assertIsNotNone(df.get_link(source_id=source_id, target_id=str(target_id)))

        dataset = PromptTestProject.get_trace_dataset_creator().create()
        layer_artifacts = dataset.artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] ==
                                                                        dataset.artifact_df[ArtifactKeys.LAYER_ID][0])
        n_clusters = 4
        clusters = {id_: str(i % n_clusters) for i, id_ in enumerate(dataset.artifact_df.index)}
        new_artifacts_df = deepcopy(dataset.artifact_df)
        for i in range(n_clusters):
            new_artifacts_df.add_artifact(str(i), "generated content")
        hgen_trace_df = TraceDataFrame()
        for source_id, artifact in layer_artifacts.itertuples():
            for target_id in range(n_clusters):
                hgen_trace_df.add_link(source_id, str(target_id), 1)

        # Without original trace df
        trace_df = HierarchyGenerator._create_trace_df_with_generated_artifacts(hgen_trace_df, new_artifacts_df)
        verify_trace_df(trace_df, len(hgen_trace_df))

        # With original trace df
        trace_df = HierarchyGenerator._create_trace_df_with_generated_artifacts(hgen_trace_df, new_artifacts_df, dataset.trace_df)
        total_traces = len(hgen_trace_df) + len(dataset.trace_df)
        verify_trace_df(trace_df, total_traces)
        for id_, trace in dataset.trace_df.itertuples():
            self.assertIsNotNone(trace_df.get_link(id_))

    def test_create_layer_df_with_generated_artifacts(self):
        # Without original layer dataframe
        expected_entities = [EnumDict({LayerKeys.SOURCE_TYPE: "source_layer", LayerKeys.TARGET_TYPE: "target_layer"})]
        hgen_layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: ["source_layer"], LayerKeys.TARGET_TYPE: ["target_layer"]})
        layer_df = HierarchyGenerator._create_layer_df_with_generated_artifacts(hgen_layer_df)
        TestAssertions.verify_entities_in_df(self, expected_entities, layer_df)

        # With original layer dataframe
        trace_dataset = PromptTestProject.get_trace_dataset_creator().create()
        layer_df = HierarchyGenerator._create_layer_df_with_generated_artifacts(hgen_layer_df,
                                                                                trace_dataset.layer_df)
        expected_entities.extend([layer for i, layer in trace_dataset.layer_df.itertuples()])
        TestAssertions.verify_entities_in_df(self, expected_entities, layer_df)

    @mock.patch("openai.Completion.create")
    @mock.patch.object(LLMResponseUtil, "extract_labels")
    def test_create_linked_dataset_for_intra_level_artifacts(self, llm_response_mock: mock.MagicMock, mock_completion: mock.MagicMock):
        llm_response_mock.return_value = self.FAKE_CLASSIFICATION_OUTPUT
        mock_completion.side_effect = fake_open_ai_completion
        artifact_df = PromptTestProject.get_artifact_project_reader().read_project()
        layer_id = artifact_df[ArtifactKeys.LAYER_ID][0]
        hgen = self.get_hierarchy_generator(self.get_tgen_trainer(self.get_dataset_creator_with_trace_dataset_creator()),
                                            layer_id=layer_id)
        linked_dataset = hgen._create_linked_dataset_for_intra_level_artifacts(artifact_df, export_path=TEST_OUTPUT_DIR).trace_dataset
        self.verify_single_layer_dataset(linked_dataset, artifact_df, layer_id)
        for label in list(linked_dataset.trace_df[TraceKeys.LABEL]):
            self.assertLess(label - 0.9, 0.1)

    def test_save_dataset_checkpoint(self):
        dataset = PromptDatasetCreator(project_reader=PromptTestProject.get_project_reader()).create()
        export_path = HierarchyGenerator.save_dataset_checkpoint(dataset, TEST_OUTPUT_DIR)
        self.assertTrue(os.path.exists(export_path))

        export_path = HierarchyGenerator.save_dataset_checkpoint(dataset, None)
        self.assertFalse(export_path)

    def test_create_trace_dataset_for_single_layer(self):
        artifact_df = PromptTestProject.get_artifact_project_reader().read_project()
        layer_id = artifact_df[ArtifactKeys.LAYER_ID][0]

        # Dont supply trace dataframe
        single_layer_trace_dataset = HierarchyGenerator._create_dataset_with_single_layer(artifact_df, layer_id).trace_dataset
        self.verify_single_layer_dataset(single_layer_trace_dataset, artifact_df, layer_id)

        # Do supply trace dataframe
        layer_artifact_ids = list(single_layer_trace_dataset.artifact_df.index)
        source, target = layer_artifact_ids[0], layer_artifact_ids[1]
        trace_df = TraceDataFrame({TraceKeys.SOURCE: [source], TraceKeys.TARGET: [target], TraceKeys.LABEL: [1]})
        single_layer_trace_dataset = HierarchyGenerator._create_dataset_with_single_layer(artifact_df, layer_id, trace_df) \
            .trace_dataset
        self.verify_single_layer_dataset(single_layer_trace_dataset, artifact_df, layer_id)
        self.assertEqual(single_layer_trace_dataset.trace_df.get_link(source_id=source, target_id=target)[TraceKeys.LABEL], 1)

    def verify_single_layer_dataset(self, dataset, artifact_df, layer_id):
        layer_artifacts = artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layer_id)
        n_layer_artifacts = len(layer_artifacts)
        expected_entites = [EnumDict({ArtifactKeys.ID: id_}) for id_ in layer_artifacts.index]
        TestAssertions.verify_entities_in_df(self, expected_entites, dataset.artifact_df)
        self.assertEqual(n_layer_artifacts * (n_layer_artifacts - 1), len(dataset))
        for id_, link in dataset.trace_df.itertuples():
            self.assertIn(link[TraceKeys.SOURCE], layer_artifacts)
            self.assertIn(link[TraceKeys.TARGET], layer_artifacts)
        self.assertEqual(1, len(dataset.layer_df))

    def test_get_target_layer_id(self):
        dataset = self.get_dataset_creator_with_trace_dataset_creator(include_summarizer=False).create()
        hgen = self.get_hierarchy_generator(tgen_trainer=None, dataset_for_sources=dataset)
        layer_id = hgen._get_target_layer_id(dataset)
        self.assertEqual(layer_id, self.TARGET_TYPE.capitalize())

        # target type is already in artifact layer ids
        dataset = self.get_dataset_creator_with_trace_dataset_creator(include_summarizer=False).create()
        dataset.trace_dataset.artifact_df.add_artifact("new_artifact", "content", self.TARGET_TYPE)
        hgen = self.get_hierarchy_generator(tgen_trainer=None, dataset_for_sources=dataset)
        layer_id = hgen._get_target_layer_id(dataset)
        self.assertNotEqual(layer_id, self.TARGET_TYPE)

    @staticmethod
    def get_tgen_trainer(dataset_creator):
        trainer_dataset_manager = TestHierarchyGeneration.get_trainer_dataset_manager(dataset_creator)
        llm_manager = OpenAIManager(llm_args=OpenAIArgs(metrics=[]))
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt2 = MultiArtifactPrompt(include_ids=False, requires_trace_link=True)
        prompt_builder = PromptBuilder(llm_manager.prompt_args, prompts=[prompt, prompt2])
        return LLMTrainer(LLMTrainerState(trainer_dataset_manager=trainer_dataset_manager, llm_manager=llm_manager,
                                          prompt_builder=prompt_builder, completion_type=LLMCompletionType.CLASSIFICATION))

    @staticmethod
    def get_trainer_dataset_manager(dataset_creator: PromptDatasetCreator):
        trainer_dataset_manager = TrainerDatasetManager(
            eval_dataset_creator=dataset_creator)
        dataset = trainer_dataset_manager[DatasetRole.EVAL]
        if dataset.artifact_df is not None:
            dataset.artifact_df = TestHierarchyGeneration.set_all_artifacts_to_same_layer(dataset.artifact_df)
            if isinstance(dataset, PromptDataset) and dataset.trace_dataset is not None:
                dataset.trace_dataset.layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [TestHierarchyGeneration.LAYER_ID],
                                                                 LayerKeys.TARGET_TYPE: [TestHierarchyGeneration.LAYER_ID]})
            elif isinstance(dataset, TraceDataset):
                dataset.layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [TestHierarchyGeneration.LAYER_ID],
                                                   LayerKeys.TARGET_TYPE: [TestHierarchyGeneration.LAYER_ID]})
        return trainer_dataset_manager

    @staticmethod
    def set_all_artifacts_to_same_layer(artifact_df):
        layer_ids = [TestHierarchyGeneration.LAYER_ID for _ in artifact_df.index]
        artifact_df[ArtifactKeys.LAYER_ID] = layer_ids
        return artifact_df

    @staticmethod
    def get_dataset_creator_with_artifact_project_reader():
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        return TestHierarchyGeneration.get_dataset_creator(project_reader=artifact_project_reader)

    @staticmethod
    def get_dataset_creator_with_prompt_project_reader(include_summarizer: bool = True):
        prompt_project_reader = PromptTestProject.get_project_reader()
        return TestHierarchyGeneration.get_dataset_creator(project_reader=prompt_project_reader, include_summarizer=include_summarizer)

    @staticmethod
    def get_dataset_creator_with_trace_dataset_creator(include_summarizer: bool = True):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        return TestHierarchyGeneration.get_dataset_creator(trace_dataset_creator=trace_dataset_creator,
                                                           include_summarizer=include_summarizer)

    @staticmethod
    def get_dataset_creator(include_summarizer: bool = True, **params):
        llm_manager = OpenAIManager(OpenAIArgs())
        return PromptDatasetCreator(summarizer=Summarizer(llm_manager) if include_summarizer else None, **params)

    def get_hierarchy_generator(self, tgen_trainer: LLMTrainer, layer_id: str = None, **params):
        llm_manager = OpenAIManager(OpenAIArgs())
        args = HGenArgs(tgen_trainer=tgen_trainer, target_type=self.TARGET_TYPE,
                        source_layer_id=self.LAYER_ID if not layer_id else layer_id, export_path=TEST_OUTPUT_DIR,
                        hgen_llm_manager=llm_manager,
                        **params)
        return HierarchyGenerator(args)
