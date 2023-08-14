from unittest import skip

from test.hgen.hgen_test_utils import get_test_hgen_args
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.hgen.hgen_args import HGenState
from tgen.hgen.steps.step_generate_inputs import GenerateInputsStep
from tgen.hgen.steps.step_initialize_dataset import InitializeDatasetStep
from tgen.testres.base_tests.base_test import BaseTest


@skip
class TestHierarchyGenerator(BaseTest):
    HGEN_ARGS = get_test_hgen_args()
    HGEN_STATE = HGenState()

    def test_run(self):
        self.assert_initialize_dataset_step()
        self.assert_generate_input_step()

    def assert_initialize_dataset_step(self):
        orig_dataset = self.HGEN_ARGS.dataset_creator_for_sources.create()
        InitializeDatasetStep().run(self.HGEN_ARGS, self.HGEN_STATE)
        self.assertSetEqual(set(self.HGEN_STATE.original_dataset.artifact_df.index), set(orig_dataset.artifact_df.index))
        for id_, artifact in self.HGEN_STATE.source_dataset.artifact_df.itertuples():
            self.assertEqual(artifact[ArtifactKeys.LAYER_ID], "C++ Code")

    def assert_generate_input_step(self):
        GenerateInputsStep().run(self.HGEN_ARGS, self.HGEN_STATE)
