import os
from unittest import mock, skip

from gen_common.constants.env_var_name_constants import PROJECT_PATH_PARAM
from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.tdatasets.idataset import iDataset
from gen_common.pipeline.abstract_pipeline import AbstractPipeline
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.pipeline.interactive_mode_options import InteractiveModeOptions
from gen_common.pipeline.state import State
from gen_common.util.file_util import FileUtil
from gen_common.util.param_specs import ParamSpecs
from gen_common.util.yaml_util import YamlUtil
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_OUTPUT_PATH
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_STATE_PATH
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.pipeline.test_state import FakeState
from gen_common_test.testprojects.safa_test_project import SafaTestProject

from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_state import HGenState
from gen.hgen.hierarchy_generator import HierarchyGenerator
from gen.hgen.steps.step_create_hgen_dataset import CreateHGenDatasetStep
from gen.hgen.steps.step_generate_artifact_content import GenerateArtifactContentStep
from gen.hgen.steps.step_generate_inputs import GenerateInputsStep
from gen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from gen_test.res.paths import TEST_OUTPUT_DIR


class TestHgenPipeline(BaseTest):
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

    @mock.patch.object(AbstractPipeline, "_option_delete_model_output")
    @mock.patch.object(AbstractPipeline, "_option_new_state")
    @mock.patch("builtins.input")
    def test_run_interactive_mode(self, input_mock: mock.MagicMock,
                                  load_new_state_mock: mock.MagicMock,
                                  delete_model_output_mock: mock.MagicMock):
        pipeline = self.get_pipeline()
        load_state_returns = [False, True]

        def fake_load_state(*args, **kwargs):
            success = load_state_returns.pop(0)
            if success:
                pipeline.state.mark_step_as_incomplete(GenerateInputsStep.get_step_name())
            return success

        interactive_mode_options = HierarchyGenerator.INTERACTIVE_MODE_OPTIONS

        re_run = interactive_mode_options.index(InteractiveModeOptions.RE_RUN)
        load_state = interactive_mode_options.index(InteractiveModeOptions.LOAD_NEW_STATE)
        next_step = interactive_mode_options.index(InteractiveModeOptions.NEXT_STEP)
        delete_model_output = interactive_mode_options.index(InteractiveModeOptions.DELETE_MODEL_OUTPUT)
        turn_off_interactive = interactive_mode_options.index(InteractiveModeOptions.TURN_OFF_INTERACTIVE) - 1
        inputs = [str(command + 1) for command in [re_run, load_state, load_state, next_step,
                                                   delete_model_output,
                                                   delete_model_output,
                                                   turn_off_interactive,
                                                   len(HierarchyGenerator.steps),
                                                   turn_off_interactive,
                                                   1]]
        input_mock.side_effect = inputs
        load_new_state_mock.side_effect = fake_load_state
        delete_model_output_mock.side_effect = [False, True]

        for option in [re_run, load_state]:
            pipeline.state.completed_steps = {InitializeDatasetStep.get_step_name(): 1, GenerateInputsStep.get_step_name(): 1}
            rerun_pipeline = pipeline._run_interactive_mode()
            self.assertTrue(rerun_pipeline)
            self.assertNotIn(GenerateInputsStep.get_step_name(), pipeline.state.completed_steps)
        self.assertEqual(load_new_state_mock.call_count, 2)
        rerun_pipeline = pipeline._run_interactive_mode()
        self.assertEqual(delete_model_output_mock.call_count, 2)
        self.assertFalse(pipeline.args.interactive_mode)
        self.assertFalse(rerun_pipeline)
        self.assertEqual(pipeline.resume_interactive_mode_step, GenerateInputsStep.get_step_name())

    @mock.patch("builtins.input")
    def test_load_new_state_from_step(self, input_mock: mock.MagicMock):
        os.environ[PROJECT_PATH_PARAM] = GEN_COMMON_TEST_PROJECT_STATE_PATH
        input_mock.side_effect = ["2", "n", str(len(HierarchyGenerator.steps) + 2)]

        pipeline = self.get_pipeline()

        pipeline.args.load_dir = GEN_COMMON_TEST_PROJECT_STATE_PATH

        success = pipeline._option_new_state(curr_step=GenerateArtifactContentStep)
        self.assertTrue(success)
        self.assertIn(GenerateInputsStep.get_step_name(), pipeline.state.completed_steps)
        success = pipeline._option_new_state(curr_step=GenerateArtifactContentStep)
        self.assertFalse(success)

    @mock.patch("builtins.input")
    @mock.patch.object(State, "load_state_from_path")
    def test_load_new_state_from_user_external_path(self, load_state_from_user_mock: mock.MagicMock, input_mock: mock.MagicMock):
        input_mock.side_effect = ["1", "bad_path", TEST_OUTPUT_DIR, GEN_COMMON_TEST_PROJECT_STATE_PATH]
        test_summary = "this worked"
        load_state_from_user_mock.side_effect = lambda path, raise_exception=False: self.fake_load_state_from_path(test_summary, path,
                                                                                                                   raise_exception)
        pipeline = self.get_pipeline()

        pipeline._option_new_state(curr_step=GenerateArtifactContentStep)
        self.assertEqual(input_mock.call_count, 4)
        self.assertEqual(pipeline.state.project_summary, test_summary)

    @mock.patch("builtins.input")
    @mock.patch("builtins.print")
    def test_display_interactive_menu(self, print_mock: mock.MagicMock, input_mock: mock.MagicMock):
        print_mock.side_effect = self.fake_print
        input_mock.side_effect = ["two"]  # ensure that bad input is handled okay
        pipeline = self.get_pipeline()

        selection = pipeline._display_interactive_menu(self.menu_options)
        self.assertEqual(selection, None)
        self.assertTrue(self.menu_options_printed)
        self.menu_options_printed = False

    @mock.patch.object(State, "delete_state_files")
    @mock.patch("builtins.input")
    def test_optional_delete_old_state_files(self, input_mock: mock.MagicMock, delete_state_files_mock: mock.MagicMock):
        pipeline = self.get_pipeline()
        deleted = pipeline._optional_delete_old_state_files(GenerateInputsStep.get_step_name())
        self.assertFalse(deleted)
        pipeline.args.load_dir = GEN_COMMON_TEST_PROJECT_STATE_PATH
        deleted = pipeline._optional_delete_old_state_files(InteractiveModeOptions.LOAD_EXTERNAL_STATE.value)
        self.assertFalse(deleted)
        deleted = pipeline._optional_delete_old_state_files(CreateHGenDatasetStep.get_step_name())
        self.assertFalse(deleted)

        input_mock.side_effect = ["n", "y"]
        deleted = pipeline._optional_delete_old_state_files(GenerateInputsStep.get_step_name())
        self.assertFalse(deleted)
        self.assertEqual(delete_state_files_mock.call_count, 0)

        deleted = pipeline._optional_delete_old_state_files(GenerateInputsStep.get_step_name())
        self.assertTrue(deleted)
        self.assertEqual(delete_state_files_mock.call_count, 1)

    @mock.patch("builtins.input")
    def test_option_delete_model_output(self, input_mock: mock.MagicMock):
        input_mock.side_effect = ["n", "y"]

        pipeline = self.get_pipeline()
        success = pipeline._option_delete_model_output()
        self.assertTrue(success)

        pipeline.args.load_dir = GEN_COMMON_TEST_PROJECT_STATE_PATH

        paths = [os.path.join(GEN_COMMON_TEST_PROJECT_STATE_PATH, "test.txt"),
                 os.path.join(GEN_COMMON_TEST_PROJECT_STATE_PATH, "test.yaml")]
        FileUtil.write("test", paths[0])
        FileUtil.write("model_output", paths[1])

        success = pipeline._option_delete_model_output()
        self.assertFalse(success)

        success = pipeline._option_delete_model_output()
        self.assertTrue(success)
        self.assertTrue(os.path.exists(paths[0]))
        self.assertFalse(os.path.exists(paths[1]))

        FileUtil.delete_file_safely(paths[0])

    def test_get_current_and_next_step(self):
        pipeline = self.get_pipeline()
        exclude_options = set()
        curr_step, next_step = pipeline._get_current_and_next_step(exclude_options)
        self.assertIsNone(curr_step)
        self.assertEqual(next_step.get_step_name(), HierarchyGenerator.steps[0].get_step_name())
        self.assertIn(InteractiveModeOptions.RE_RUN.name, exclude_options)
        pipeline.state.completed_steps = {GenerateInputsStep.get_step_name(): 1, CreateHGenDatasetStep.get_step_name(): 1}
        exclude_options = set()
        curr_step, next_step = pipeline._get_current_and_next_step(exclude_options)
        self.assertIsNone(next_step)
        self.assertSize(0, exclude_options)
        self.assertEqual(curr_step.get_step_name(), CreateHGenDatasetStep.get_step_name())

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
        expected_path = FileUtil.collapse_paths(GEN_COMMON_TEST_OUTPUT_PATH)
        self.assertEqual(reloaded_attrs["export_dir"], expected_path)
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

    def get_pipeline(self):
        args = HGenArgs(source_layer_ids="source", target_type="target",
                        dataset_creator=PromptDatasetCreator(
                            trace_dataset_creator=TraceDatasetCreator(SafaTestProject.get_project_reader())))
        return HierarchyGenerator(args)
