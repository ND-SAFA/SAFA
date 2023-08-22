import os

from test.hgen.hgen_test_utils import HGenTestConstants
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.yaml_util import YamlUtil
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.state.state import State
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR, TEST_STATE_PATH


class TestState(BaseTest):

    def test_get_path_to_state_checkpoint(self):
        with_checkpoint = os.path.join(TEST_OUTPUT_DIR, "state_checkpoints")
        self.assertEqual(State._get_path_to_state_checkpoint(with_checkpoint), with_checkpoint)

        without_checkpoint = TEST_OUTPUT_DIR
        self.assertEqual(State._get_path_to_state_checkpoint(without_checkpoint), with_checkpoint)

        self.assertEqual(State._get_path_to_state_checkpoint(without_checkpoint, "StepName"),
                         os.path.join(with_checkpoint, "state-step-name.yaml"))

    def test_load_latest(self):
        steps = [step.get_step_name() for step in HierarchyGenerator.steps]
        state = HGenState.load_latest(TEST_STATE_PATH, steps)
        self.assertSetEqual(set(steps), state.completed_steps)
        self.assertEqual(state.description_of_artifact, HGenTestConstants.description)
        self.assertEqual(state.summary, HGenTestConstants.summary)
        self.assertListEqual(state.questions, HGenTestConstants.questions.splitlines())
        self.assertListEqual(state.generated_artifact_content, HGenTestConstants.user_stories)
        self.assertEqual(state.format_of_artifacts, HGenTestConstants.format_)
        self.assertIsInstance(state.original_dataset, PromptDataset)
        self.assertIsInstance(state.source_dataset, PromptDataset)
        self.assertIsInstance(state.dataset, TraceDataset)

        # failed to find a state so initialize empty
        file_not_found_state = HGenState.load_latest(TEST_STATE_PATH, ["UnknownStep"])
        self.assertSize(0, file_not_found_state.completed_steps)

        failed_state = HGenState.load_latest(TEST_STATE_PATH, ["BadFile"])
        self.assertSize(0, failed_state.completed_steps)

    def test_save(self):
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

        self.assertSetEqual(orig_state.completed_steps, reloaded_attrs["completed_steps"])
        self.assertEqual(orig_state.description_of_artifact, reloaded_attrs["description_of_artifact"])
        self.assertEqual(orig_state.summary, reloaded_attrs["summary"])
        self.assertListEqual(orig_state.questions, reloaded_attrs["questions"])
        self.assertListEqual(orig_state.generated_artifact_content, reloaded_attrs["generated_artifact_content"])
        self.assertEqual(orig_state.format_of_artifacts, reloaded_attrs["format_of_artifacts"])
        reloaded_dataset_original = assert_check_type("original_dataset", reloaded_attrs["original_dataset"],)
        self.assertSetEqual(set(orig_state.original_dataset.artifact_df.index), set(reloaded_dataset_original.artifact_df.index))
        reloaded_dataset_source = assert_check_type("source_dataset", reloaded_attrs["source_dataset"])
        self.assertSetEqual(set(orig_state.source_dataset.artifact_df.index), set(reloaded_dataset_source.artifact_df.index))
        self.assertEqual(orig_state.dataset, reloaded_attrs["dataset"])
