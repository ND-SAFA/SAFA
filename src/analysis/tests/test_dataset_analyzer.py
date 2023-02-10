from analysis.dataset_analyzer import DatasetAnalyzer
from data.datasets.trace_dataset import TraceDataset
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from testres.base_test import BaseTest


class TestDatasetAnalyzer(BaseTest):
    a1_body = "Artifact body with no out_of_vocabulary  words."
    a2_body = "Here Betito is introducing some unknown words like HVAC."
    a3_body = "Another 1.0 is just for funsies!"
    expected_oov_words = {"betito", "hvac", "funsies"}

    def test_get_oov_words(self):
        model_manager = ModelManager("bert-base-uncased")
        analyzer = self.get_dataset_analyzer()
        oov = analyzer.get_oov_words(model_manager)
        self.assertSetEqual(oov, self.expected_oov_words)

    def get_dataset_analyzer(self):
        a1 = Artifact("s1", self.a1_body)
        a2 = Artifact("s2", self.a2_body)
        a3 = Artifact("s3", self.a3_body)

        l1 = TraceLink(a1, a2)
        l2 = TraceLink(a1, a3)

        links = {l1.id: l1, l2.id: l2}

        dataset = TraceDataset(links, [l1.id, l2.id], [])

        return DatasetAnalyzer(dataset)
