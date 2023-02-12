from analysis import word_tools
from analysis.dataset_analyzer import DatasetAnalyzer
from data.datasets.trace_dataset import TraceDataset
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from testres.base_test import BaseTest
from testres.paths.paths import TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
from util.json_util import JsonUtil


class TestDatasetAnalyzer(BaseTest):
    a1_body = "Artifact body with no out_of_vocabulary words."
    a2_body = "Here we introduce some unknown words like hvac and funsies."
    a3_body = "Another 1.0 from Betito just for funsies and more funsies!"
    EXPECTED_HIGH_FREQ_WORDS = ["words", "funsies"]

    def test_save(self):
        analyzer = self.get_dataset_analyzer(lengthen=True)
        save_path = analyzer.analyze_and_save(TEST_OUTPUT_DIR)
        output = JsonUtil.read_json_file(save_path)
        self.assertIn(DatasetAnalyzer.READABILITY_SCORE, output)
        self.assertIn(DatasetAnalyzer.HIGH_FREQUENCY_WORDS, output)
        self.assertIn(DatasetAnalyzer.LOW_FREQUENCY_WORDS, output)
        self.assertIn(DatasetAnalyzer.OOV_WORDS.format("bert-base-uncased"), output)
        
    def test_get_readability_score(self):
        analyzer = self.get_dataset_analyzer(lengthen=True)
        readability_score = analyzer.get_readability_score()
        self.assertGreater(readability_score, 0)

    def test_get_high_frequency_word_counts(self):
        analyzer = self.get_dataset_analyzer()
        expected_low_freq_words = [word for body in [self.a1_body, self.a2_body, self.a3_body] for word in body.split()
                                   if word not in self.EXPECTED_HIGH_FREQ_WORDS and word not in word_tools.STOP_WORDS]
        expected_proportion = 0.64
        low_freq_words, proportion = analyzer.get_low_frequency_word_counts(0.1)
        TestAssertions.assert_lists_have_the_same_vals(self, expected_low_freq_words, low_freq_words)
        self.assertLessEqual(abs(proportion - expected_proportion), 0.01)

    def test_get_high_frequency_word_counts(self):
        analyzer = self.get_dataset_analyzer()
        expected_proportion = 0.35
        high_freq_words, proportion = analyzer.get_high_frequency_word_counts(0.1)
        TestAssertions.assert_lists_have_the_same_vals(self, self.EXPECTED_HIGH_FREQ_WORDS, high_freq_words)
        self.assertLessEqual(abs(proportion - expected_proportion), 0.01)

    def test_get_oov_words(self):
        analyzer = self.get_dataset_analyzer()
        oov = analyzer.get_oov_words(analyzer.model_managers[0])
        expected_oov_words = {"betito": 1, "hvac": 1, "funsies": 3}
        self.assertDictEqual(oov, expected_oov_words)

    def test_get_vocab(self):
        artifact_bodies = [self.a1_body, self.a2_body, self.a3_body]
        artifact_bodies = word_tools.CLEANER.run(artifact_bodies)
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
        a2 = Artifact("t2", artifact_bodies[1])
        a3 = Artifact("t3", artifact_bodies[2])

        l1 = TraceLink(a1, a2)
        l2 = TraceLink(a1, a3)

        links = {l1.id: l1, l2.id: l2}

        dataset = TraceDataset(links, [l1.id, l2.id], [])
        return DatasetAnalyzer(dataset, [ModelManager("bert-base-uncased"), ModelManager("prajjwal1/bert-tiny")])
