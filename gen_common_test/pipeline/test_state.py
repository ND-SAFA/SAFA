import os
from dataclasses import dataclass
from os.path import dirname
from typing import Union
from unittest import skip

from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.tdatasets.idataset import iDataset
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.pipeline.state import State
from gen_common.util.param_specs import ParamSpecs
from gen_common.util.reflection_util import ReflectionUtil
from gen_common.util.yaml_util import YamlUtil
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_DIR_PATH, GEN_COMMON_TEST_OUTPUT_PATH
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_STATE_PATH
from gen_common_test.base.tests.base_test import BaseTest


@dataclass
class FakeState(State):
    original_dataset: Union[PromptDataset, TraceDataset] = None
    final_dataset: PromptDataset = None
    property1: int = None
    property2: str = None


class TestState(BaseTest):

    def test_get_path_to_state_checkpoint(self):
        with_checkpoint = os.path.join(GEN_COMMON_TEST_OUTPUT_PATH, "state_checkpoints")
        self.assertEqual(State.get_path_to_state_checkpoint(with_checkpoint), with_checkpoint)

        without_checkpoint = GEN_COMMON_TEST_OUTPUT_PATH
        self.assertEqual(State.get_path_to_state_checkpoint(without_checkpoint), with_checkpoint)

        self.assertEqual(State.get_path_to_state_checkpoint(without_checkpoint, "StepName"),
                         os.path.join(with_checkpoint, "state-step-name.yaml"))

    def test_load_latest(self):
        os.environ["ROOT_PATH"] = dirname(GEN_COMMON_TEST_DIR_PATH)
        steps = ["Step1", "Step2", "Step3"]
        state = FakeState.load_latest(GEN_COMMON_TEST_PROJECT_STATE_PATH, steps)
        self.assertEqual(state.export_dir, GEN_COMMON_TEST_OUTPUT_PATH)
        self.assertSetEqual(set(steps), set(state.completed_steps.keys()))
        self.assertIsInstance(state.original_dataset, PromptDataset)
        self.assertIsInstance(state.final_dataset, PromptDataset)

        # failed to find a state so initialize empty
        file_not_found_state = FakeState.load_latest(GEN_COMMON_TEST_PROJECT_STATE_PATH, ["UnknownStep"])
        self.assertSize(0, file_not_found_state.completed_steps)

        failed_state = FakeState.load_latest(GEN_COMMON_TEST_PROJECT_STATE_PATH, ["BadFile"])
        self.assertSize(0, failed_state.completed_steps)

    @skip
    def test_save(self):

        def assert_check_type(name, val):
            if isinstance(val, AbstractDatasetCreator):
                val = FakeState._check_type(name, val, param_specs)
                self.assertIsInstance(val, iDataset)
            return val

        state_name = "Step2"
        step_num = 2
        orig_path = State.get_path_to_state_checkpoint(GEN_COMMON_TEST_PROJECT_STATE_PATH, state_name, step_num=step_num)
        attrs = YamlUtil.read(orig_path)
        param_specs = ParamSpecs.create_from_method(HGenState.__init__)
        checked_attrs = {}
        for name, val in attrs.items():
            checked_attrs[name] = assert_check_type(name, val)
        orig_state = FakeState(**checked_attrs)
        orig_state.export_dir = GEN_COMMON_TEST_OUTPUT_PATH
        orig_state.save(state_name)
        save_path = State.get_path_to_state_checkpoint(GEN_COMMON_TEST_OUTPUT_PATH, state_name, step_num=step_num)
        reloaded_attrs = YamlUtil.read(save_path)
        self.assertEqual(reloaded_attrs["export_dir"], '[ROOT_PATH]/gen_common_test/test_data/output')
        self.assertDictEqual(orig_state.completed_steps, reloaded_attrs["completed_steps"])
        reloaded_dataset_original = assert_check_type("original_dataset", reloaded_attrs["original_dataset"], )
        self.assertSetEqual(set(orig_state.original_dataset.artifact_df.index), set(reloaded_dataset_original.artifact_df.index))
        self.assertEqual(orig_state.final_dataset, reloaded_attrs["final_dataset"])
        self.assertEqual(orig_state.property1, reloaded_attrs["property1"])
        self.assertEqual(orig_state.property2, reloaded_attrs["property2"])

        orig_state.save(state_name, attrs2ignore={"final_dataset"})
        reloaded_attrs = YamlUtil.read(save_path)
        self.assertNotIn("final_dataset", reloaded_attrs)
        try:
            orig_state.load_state_from_path(save_path, raise_exception=True)
        except Exception as e:
            self.fail(e)

    def test_mark_as_complete(self):
        state = FakeState()
        step_name = "Step2"
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
