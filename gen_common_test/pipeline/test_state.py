import os
from dataclasses import dataclass
from typing import Union

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.pipeline.state import State
from gen_common.util.reflection_util import ReflectionUtil
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_OUTPUT_PATH
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
        os.environ["PROJECT_PATH"] = GEN_COMMON_TEST_PROJECT_STATE_PATH
        steps = ["Step1", "Step2", "Step3"]
        state = FakeState.load_latest(GEN_COMMON_TEST_PROJECT_STATE_PATH, steps)
        self.assertEqual(state.export_dir, os.path.join(GEN_COMMON_TEST_PROJECT_STATE_PATH, "output"))
        self.assertSetEqual(set(steps), set(state.completed_steps.keys()))
        self.assertIsInstance(state.original_dataset, PromptDataset)
        self.assertIsInstance(state.final_dataset, PromptDataset)

        # failed to find a state so initialize empty
        file_not_found_state = FakeState.load_latest(GEN_COMMON_TEST_PROJECT_STATE_PATH, ["UnknownStep"])
        self.assertSize(0, file_not_found_state.completed_steps)

        failed_state = FakeState.load_latest(GEN_COMMON_TEST_PROJECT_STATE_PATH, ["BadFile"])
        self.assertSize(0, failed_state.completed_steps)

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
