from data.datasets.dataset_role import DatasetRole
from data.datasets.trace_dataset import TraceDataset
from testres.base_trace_test import BaseTraceTest
from variables.typed_definition_variable import TypedDefinitionVariable


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
        self.assertEquals(len(datasets_container[DatasetRole.TRAIN].pos_link_ids),
                          len(datasets_container[DatasetRole.TRAIN].neg_link_ids))
