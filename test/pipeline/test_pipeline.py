from unittest import mock

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, AbstractPipeline
from tgen.state.pipeline.interactive_mode_options import InteractiveModeOptions
from tgen.state.state import State
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_HGEN_PATH, TEST_STATE_PATH, TEST_OUTPUT_DIR


class TestPipeline(BaseTest):
    menu_options = [InteractiveModeOptions.NEXT_STEP, InteractiveModeOptions.QUIT]
    menu_options_printed = False
    curr_step_index = 1

    def fake_run_step(self, step: AbstractPipelineStep, re_run: bool = False):
        self.assertIsInstance(step, HierarchyGenerator.steps[self.curr_step_index].__class__)
        self.assertTrue(re_run)

    def fake_load_state_from_path(self, test_summary: str, path: str, raise_exception: bool = False):
        if path == TEST_OUTPUT_DIR:
            return Exception()
        return HGenState(project_summary=test_summary)

    def fake_print(self, str2print, *args, sep=' ', end='\n', file=None):
        if self.menu_options[0].value in str2print:
            success = True
            for opt in self.menu_options:
                if opt.value not in str2print:
                    success = False
                self.menu_options_printed = success

    @mock.patch.object(AbstractPipeline, "_load_new_state_from_user")
    @mock.patch("builtins.input")
    @mock.patch.object(AbstractPipelineStep, "run")
    def test_run_interactive_mode(self, run_step_mock: mock.MagicMock, input_mock: mock.MagicMock,
                                  load_new_state_mock: mock.MagicMock):
        input_mock.side_effect = ["1", "2", "4", "3"]
        test_summary = "this worked"
        load_new_state_mock.return_value = HGenState(project_summary=test_summary, completed_steps={step.get_step_name(): 1
                                                                                                    for step in HierarchyGenerator.steps})

        pipeline = self.get_pipeline()
        pipeline._run_interactive_mode(pipeline.steps[self.curr_step_index])
        self.assertEqual(run_step_mock.call_count, 1)

        pipeline = self.get_pipeline()
        self.assertFalse(pipeline.state.step_is_complete(pipeline.steps[self.curr_step_index + 1]))
        pipeline._run_interactive_mode(pipeline.steps[self.curr_step_index])
        self.assertTrue(pipeline.state.step_is_complete(pipeline.steps[self.curr_step_index + 1].get_step_name()))

        pipeline = self.get_pipeline()
        pipeline._run_interactive_mode(pipeline.steps[self.curr_step_index])
        self.assertEqual(pipeline.state.project_summary, test_summary)
        self.assertTrue(pipeline.state.step_is_complete(pipeline.steps[self.curr_step_index].get_step_name()))
        self.assertFalse(pipeline.state.step_is_complete(pipeline.steps[len(HierarchyGenerator.steps)-1].get_step_name()))

    @mock.patch("builtins.input")
    @mock.patch.object(State, "load_state_from_path")
    def test_load_new_state_from_user(self, load_state_from_user_mock: mock.MagicMock, input_mock: mock.MagicMock):
        input_mock.side_effect = ["bad_path", TEST_OUTPUT_DIR, TEST_STATE_PATH, "b"]
        test_summary = "this worked"
        load_state_from_user_mock.side_effect = lambda path, raise_exception=False: self.fake_load_state_from_path(test_summary, path,
                                                                                                                   raise_exception)
        pipeline = self.get_pipeline()

        state: HGenState = pipeline._load_new_state_from_user(HGenState())
        self.assertEqual(input_mock.call_count, 3)
        self.assertEqual(state.project_summary, test_summary)

        state: None = pipeline._load_new_state_from_user(HGenState())
        self.assertIsNone(state)

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_display_interactive_menu(self, print_mock: mock.MagicMock, input_mock: mock.MagicMock):
        print_mock.side_effect = self.fake_print
        input_mock.side_effect = ["two", "3", "2"]  # ensure that bad input is handled okay
        pipeline = self.get_pipeline()

        selection = pipeline._display_interactive_menu(self.menu_options)
        self.assertEqual(selection, self.menu_options[1])
        self.assertTrue(self.menu_options_printed)
        self.assertEqual(input_mock.call_count, 3)
        self.menu_options_printed = False

    def get_pipeline(self):
        args = HGenArgs(source_layer_id="source", target_type="target", dataset=TraceDatasetCreator(TEST_HGEN_PATH))
        return HierarchyGenerator(args)
