from analysis.link_analyzer import LinkAnalyzer
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from testres.base_test import BaseTest
from testres.paths.paths import TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
from util.json_util import JsonUtil


class TestLinkAnalyzer(BaseTest):
    a1_body = "This is a really small artifact body to use as a test."
    a2_body = "This is a really large artifct body to try out for funsies."
    expected_oov_words = {"funsies": 1, "artifct": 1}
    expected_analyses = [LinkAnalyzer.COMMON_WORDS, LinkAnalyzer.MISSPELLED_WORDS, LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS,
                         LinkAnalyzer.OOV_WORDS]
    expected_counts = {name: 2 for name in expected_analyses}

    def test_get_analysis_counts(self):
        analyzer = self.get_link_analyzer()
        analysis = analyzer.get_analysis_counts()
        for analysis_name in self.expected_counts.keys():
            self.assertIn(analysis_name, analysis)
            self.assertEquals(analysis[analysis_name], self.expected_counts[analysis_name])

    def test_get_analysis(self):
        analyzer = self.get_link_analyzer()
        analysis = analyzer.get_analysis()
        for analysis_name in self.expected_analyses:
            self.assertIn(analysis_name, analysis)

    def test_save(self):
        analyzer = self.get_link_analyzer()
        output_path = analyzer.save(TEST_OUTPUT_DIR)
        output_dict = JsonUtil.read_json_file(output_path)
        self.assertIn(analyzer.ARTIFACT_TOKENS, output_dict)
        self.assertIn(analyzer.ANALYSIS, output_dict)
        expected_analyses = [analyzer.COMMON_WORDS, analyzer.MISSPELLED_WORDS, analyzer.SHARED_SYNONYMS_AND_ANTONYMS,
                             analyzer.OOV_WORDS]
        for analysis in expected_analyses:
            self.assertIn(analysis, output_dict[analyzer.ANALYSIS])

    def test_get_words_in_common(self):
        expected_words_in_common = {"really", "body"}
        analyzer = self.get_link_analyzer()
        self.assertSetEqual(analyzer.get_words_in_common(), expected_words_in_common)

    def test_get_misspelled_words(self):
        analyzer = self.get_link_analyzer()
        misspelled = analyzer.get_misspelled_words()
        self.assertDictEqual(misspelled, self.expected_oov_words)

    def test_get_shared_synonyms_and_antonyms(self):
        analyzer = self.get_link_analyzer()
        syn_and_ant = analyzer.get_shared_synonyms_and_antonyms()
        self.assertIn('try', syn_and_ant)
        self.assertIn('large', syn_and_ant)

    def test_get_oov_vocab(self):
        analyzer = self.get_link_analyzer()
        oov = analyzer.get_oov_words(analyzer.model_manager)
        self.assertDictEqual(oov, self.expected_oov_words)

    def test_get_artifact_vocab(self):
        analyzer = self.get_link_analyzer()
        artifact = analyzer.link.source
        vocab = analyzer.get_artifact_vocab(artifact)
        expected_vocab = self.a1_body[:-1].lower().split()
        TestAssertions.assert_lists_have_the_same_vals(self, vocab, expected_vocab)

    def test_get_synonyms_and_antonyms(self):
        analyzer = self.get_link_analyzer()
        synonyms, antonyms = analyzer._get_synonyms_and_antonyms(analyzer.word_counts[0])
        self.assertIn("try_out", synonyms)
        self.assertIn("large", antonyms)

    def get_link_analyzer(self):
        a1 = Artifact("s1", self.a1_body)
        a2 = Artifact("t1", self.a2_body)
        return LinkAnalyzer(TraceLink(a1, a2), ModelManager('bert-base-uncased'))
