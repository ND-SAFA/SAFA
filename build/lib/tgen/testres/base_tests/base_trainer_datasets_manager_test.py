from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.testres.base_tests.base_trace_test import BaseTraceTest
from common_resources.tools.variables.typed_definition_variable import TypedDefinitionVariable


class BaseTrainerDatasetsManagerTest(BaseTraceTest):
    val_dataset_creator_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
        "val_percentage": 0.3
    }
    eval_dataset_creator_definition = {
        TypedDefinitionVariable.OBJECT_TYPE_KEY: "SPLIT",
        "val_percentage": 0.2
    }

    def assert_final_datasets_are_as_expected(self, datasets_container, include_pretrain=True):
        expected_dataset_split_roles = [DatasetRole.TRAIN, DatasetRole.VAL, DatasetRole.EVAL]
        for dataset_role in expected_dataset_split_roles:
            self.assertIn(dataset_role, datasets_container)
            self.assertTrue(isinstance(datasets_container[dataset_role], TraceDataset))
        if include_pretrain:
            self.assertIn(DatasetRole.PRE_TRAIN, datasets_container)
        train_dataset = datasets_container[DatasetRole.TRAIN]
        self.assertEqual(len(train_dataset.get_pos_link_ids()),
                         len(train_dataset.get_neg_link_ids()))
