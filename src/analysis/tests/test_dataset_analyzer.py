from analysis.dataset_analyzer import DatasetAnalyzer
from data.datasets.trace_dataset import TraceDataset
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from testres.base_test import BaseTest
from testres.test_assertions import TestAssertions


class TestDatasetAnalyzer(BaseTest):
    a1_body = "Artifact body with no out_of_vocabulary words."
    a2_body = "Here Betito is introducing some unknown words like hvac and funsies."
    a3_body = "Another 1.0 just for funsies and more funsies!"
    expected_high_freq_words = ["words", "funsies"]

    def test_get_readability_score(self):
        analyzer = self.get_dataset_analyzer(lengthen=True)
        readability_score = analyzer.get_readability_score()
        self.assertGreater(readability_score, 0)

    def test_get_high_frequency_word_counts(self):
        analyzer = self.get_dataset_analyzer()
        expected_low_freq_words = [word for body in [self.a1_body, self.a2_body, self.a3_body] for word in body.split()
                                   if word not in self.expected_high_freq_words and word not in DatasetAnalyzer.STOP_WORDS]
        expected_proportion = 0.64
        low_freq_words, proportion = analyzer.get_low_frequency_word_counts(0.1)
        TestAssertions.assert_lists_have_the_same_vals(self, expected_low_freq_words, low_freq_words)
        self.assertLessEqual(abs(proportion - expected_proportion), 0.01)

    def test_get_high_frequency_word_counts(self):
        analyzer = self.get_dataset_analyzer()
        expected_proportion = 0.35
        high_freq_words, proportion = analyzer.get_high_frequency_word_counts(0.1)
        TestAssertions.assert_lists_have_the_same_vals(self, self.expected_high_freq_words, high_freq_words)
        self.assertLessEqual(abs(proportion - expected_proportion), 0.01)

    def test_get_oov_words(self):
        model_manager = ModelManager("bert-base-uncased")
        analyzer = self.get_dataset_analyzer()
        oov = analyzer.get_oov_words(model_manager)
        expected_oov_words = {"betito": 1, "hvac": 1, "funsies": 3}
        self.assertDictEqual(oov, expected_oov_words)

    def test_get_vocab(self):
        artifact_bodies = [self.a1_body, self.a2_body, self.a3_body]
        artifact_bodies = DatasetAnalyzer.CLEANER.run(artifact_bodies)
        expected_vocab = []
        for a_bod in artifact_bodies:
            expected_vocab.extend([word.lower() for word in a_bod.split()])
        analyzer = self.get_dataset_analyzer()
        vocab = analyzer._get_vocab()
        TestAssertions.assert_lists_have_the_same_vals(self, vocab, expected_vocab)

    def get_dataset_analyzer(self, lengthen: bool = False):
        artifact_bodies = [self.a1_body, self.a2_body, self.a3_body]
        if lengthen:
            lengthened_artifact_bodies = []
            for a_bod in artifact_bodies:
                a_bod_long = " ".join([a_bod for i in range(4)])
                lengthened_artifact_bodies.append(a_bod_long)
            artifact_bodies = lengthened_artifact_bodies

        a1 = Artifact("s1", artifact_bodies[0])
        a2 = Artifact("s2", artifact_bodies[1])
        a3 = Artifact("s3", artifact_bodies[2])

        l1 = TraceLink(a1, a2)
        l2 = TraceLink(a1, a3)

        links = {l1.id: l1, l2.id: l2}

        dataset = TraceDataset(links, [l1.id, l2.id], [])

        return DatasetAnalyzer(dataset)
