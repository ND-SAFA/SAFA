import os

from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_DATA_DIR
from tracer.datasets.creators.safa_dataset_creator import SafaDatasetCreator
from tracer.datasets.formats.safa_format import SafaFormat


class TestSafaDatasetCreator(BaseTraceTest):
    TRACE_FILES_2_ARTIFACTS = {"Layer1Source2Target.json": ("Layer1Source.json", "Layer1Target.json"),
                               "Layer2Source2Target.json": ("Layer2Source.json", "Layer2Target.json"),
                               }
    KEYS = SafaFormat(trace_files_2_artifacts=TRACE_FILES_2_ARTIFACTS)
    SAFA_DATA_DIR = os.path.join(TEST_DATA_DIR, "safa")

    def test_create(self):
        dataset_creator = self.get_safa_dataset_creator()
        dataset = dataset_creator.create()
        self.assert_lists_have_the_same_vals(dataset.pos_link_ids, self.get_link_ids(self.POS_LINKS))
        self.assert_lists_have_the_same_vals(dataset.links, self.get_link_ids(self.ALL_TEST_LINKS))
        self.assert_lists_have_the_same_vals(dataset.neg_link_ids, self.get_link_ids(self.NEG_LINKS))

    def test_create_artifacts_from_file(self):
        dataset_creator = self.get_safa_dataset_creator()
        sources = []
        for source_file, target_file in self.TRACE_FILES_2_ARTIFACTS.values():
            sources += dataset_creator._create_artifacts_from_file(source_file)
        self.assert_lists_have_the_same_vals(list(self.SOURCE_LAYERS[0].keys()) + list(self.SOURCE_LAYERS[1].keys()),
                                             [artifact.id for artifact in sources])

    def test_get_pos_link_ids_from_file(self):
        dataset_creator = self.get_safa_dataset_creator()
        pos_link_ids = []
        for trace_file in self.TRACE_FILES_2_ARTIFACTS.keys():
            pos_link_ids += dataset_creator._get_pos_link_ids_from_file(trace_file)
        self.assert_lists_have_the_same_vals(pos_link_ids, self.get_link_ids(self.POS_LINKS))

    def get_safa_dataset_creator(self):
        return SafaDatasetCreator(self.SAFA_DATA_DIR, self.DATA_CLEANING_STEPS, data_keys=self.KEYS)
