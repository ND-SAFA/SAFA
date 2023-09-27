import os
from unittest import mock
from unittest.mock import MagicMock

from test.hgen.hgen_test_utils import HGenTestConstants
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.yaml_util import YamlUtil
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.delta.delta_state import DeltaState
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.state.state import State
from tgen.summarizer.projects.project_summarizer import ProjectSummarizer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.paths.paths import TEST_OUTPUT_DIR, TEST_STATE_PATH
from tgen.tracing.ranking.ranking_state import RankingState


class TestState(BaseTest):

    def test_get_path_to_state_checkpoint(self):
        with_checkpoint = os.path.join(TEST_OUTPUT_DIR, "state_checkpoints")
        self.assertEqual(State._get_path_to_state_checkpoint(with_checkpoint), with_checkpoint)

        without_checkpoint = TEST_OUTPUT_DIR
        self.assertEqual(State._get_path_to_state_checkpoint(without_checkpoint), with_checkpoint)

        self.assertEqual(State._get_path_to_state_checkpoint(without_checkpoint, "StepName"),
                         os.path.join(with_checkpoint, "state-step-name.yaml"))

    @mock.patch.object(ProjectSummarizer, "summarize")
    @mock_anthropic
    def test_load_latest(self, anthropic_manager: TestAIManager, project_summary_mock: MagicMock):
        project_summary_mock.return_value = "project_summary"
        anthropic_manager.mock_summarization()
        steps = [step.get_step_name() for step in HierarchyGenerator.steps if step.get_step_name()]
        state = HGenState.load_latest(TEST_STATE_PATH, steps)
        self.assertSetEqual(set(steps), set(state.completed_steps.keys()))
        self.assertEqual(state.description_of_artifact, HGenTestConstants.description)
        self.assertEqual(state.summary, HGenTestConstants.summary)
        self.assertListEqual(state.questions, HGenTestConstants.questions.splitlines())
        self.assertSetEqual(set(state.generation_predictions.keys()), set(HGenTestConstants.user_stories))
        self.assertListEqual(list(state.generation_predictions.values()), HGenTestConstants.code_files)
        self.assertEqual(state.format_of_artifacts, HGenTestConstants.format_)
        self.assertIsInstance(state.original_dataset, PromptDataset)
        self.assertIsInstance(state.source_dataset, PromptDataset)
        self.assertIsInstance(state.final_dataset, PromptDataset)

        # failed to find a state so initialize empty
        file_not_found_state = HGenState.load_latest(TEST_STATE_PATH, ["UnknownStep"])
        self.assertSize(0, file_not_found_state.completed_steps)

        failed_state = HGenState.load_latest(TEST_STATE_PATH, ["BadFile"])
        self.assertSize(0, failed_state.completed_steps)

    @mock.patch.object(ProjectSummarizer, "summarize")
    @mock_anthropic
    def test_save(self, anthropic_manager: TestAIManager, project_summary_mock: MagicMock):
        project_summary_mock.return_value = "project_summary"
        anthropic_manager.mock_summarization()

        def assert_check_type(name, val):
            if isinstance(val, AbstractDatasetCreator):
                val = HGenState._check_type(name, val, param_specs)
                self.assertIsInstance(val, iDataset)
            return val

        state_name = GenerateArtifactContentStep.get_step_name()
        attrs = YamlUtil.read(State._get_path_to_state_checkpoint(TEST_STATE_PATH, state_name))
        param_specs = ParamSpecs.create_from_method(HGenState.__init__)
        checked_attrs = {}
        for name, val in attrs.items():
            checked_attrs[name] = assert_check_type(name, val)
        orig_state = HGenState(**checked_attrs)
        orig_state.export_dir = TEST_OUTPUT_DIR
        orig_state.save(state_name)
        reloaded_attrs = YamlUtil.read(State._get_path_to_state_checkpoint(TEST_OUTPUT_DIR, state_name))
        self.assertEqual(reloaded_attrs["export_dir"], '[ROOT_PATH]/testres/output')
        self.assertDictEqual(orig_state.completed_steps, reloaded_attrs["completed_steps"])
        self.assertEqual(orig_state.description_of_artifact, reloaded_attrs["description_of_artifact"])
        self.assertEqual(orig_state.summary, reloaded_attrs["summary"])
        self.assertListEqual(orig_state.questions, reloaded_attrs["questions"])
        self.assertDictEqual(orig_state.generation_predictions, reloaded_attrs["generation_predictions"])
        self.assertEqual(orig_state.format_of_artifacts, reloaded_attrs["format_of_artifacts"])
        reloaded_dataset_original = assert_check_type("original_dataset", reloaded_attrs["original_dataset"], )
        self.assertSetEqual(set(orig_state.original_dataset.artifact_df.index), set(reloaded_dataset_original.artifact_df.index))
        reloaded_dataset_source = assert_check_type("source_dataset", reloaded_attrs["source_dataset"])
        self.assertSetEqual(set(orig_state.source_dataset.artifact_df.index), set(reloaded_dataset_source.artifact_df.index))
        self.assertEqual(orig_state.final_dataset, reloaded_attrs["final_dataset"])

    def test_mark_as_complete(self):
        state = HGenState()
        step_name = GenerateArtifactContentStep.get_step_name()
        self.assertFalse(state.step_is_complete(step_name))
        state.mark_step_as_complete(step_name)
        self.assertTrue(state.step_is_complete(step_name))
        state.mark_step_as_complete(step_name)
        self.assertEqual(state.completed_steps[step_name], 2)
        state.mark_step_as_incomplete(step_name)
        self.assertFalse(state.step_is_complete(step_name))

    def test_is_a_path_variable(self):
        path_vars = {k for k, v in vars(State).items() if not ReflectionUtil.is_function(v) and State._is_a_path_variable(k)}
        self.assertEqual(len(path_vars), 1)
        self.assertIn('export_dir', path_vars)