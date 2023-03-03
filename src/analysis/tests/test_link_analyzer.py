# from copy import deepcopy
# from unittest import skip
#
# from analysis.link_analyzer import LinkAnalyzer
# from data.tree.artifact import Artifact
# from data.tree.trace_dataframe import TraceDataFrame
# from models.model_manager import ModelManager
# from testres.base_test import BaseTest
# from testres.paths.paths import TEST_OUTPUT_DIR
# from testres.test_assertions import TestAssertions
# from util.json_util import JsonUtil
#
#
# @skip("Skipping analysis because, well, it was a failure.")
# class TestLinkAnalyzer(BaseTest):
#     a1_body = "This is a really small artifact body to use as a test rationally."
#     a2_body = "This is a really large artifct body to try out for funsies."
#     EXPECTED_MISSPELLED_WORDS = {"funsies": 1, "artifct": 1}
#     EXPECTED_OOV_WORDS = {"rationally": 1}
#     EXPECTED_ANALYSES = [LinkAnalyzer.COMMON_WORDS, LinkAnalyzer.MISSPELLED_WORDS, LinkAnalyzer.SHARED_ANTONYMS,
#                          LinkAnalyzer.SHARED_SYNONYMS, LinkAnalyzer.OOV_WORDS]
#     EXPECTED_COUNTS = {name: 1 for name in EXPECTED_ANALYSES[2:]}
#     EXPECTED_COUNTS[LinkAnalyzer.COMMON_WORDS] = 2
#     EXPECTED_COUNTS[LinkAnalyzer.MISSPELLED_WORDS] = 2
#
#     def test_get_analysis_counts(self):
#         analyzer = self.get_link_analyzer()
#         analysis = analyzer.get_category_counts()
#         for analysis_name in self.EXPECTED_COUNTS.keys():
#             self.assertIn(analysis_name, analysis)
#             self.assertEquals(analysis[analysis_name], self.EXPECTED_COUNTS[analysis_name])
#
#     def test_get_analysis(self):
#         analyzer = self.get_link_analyzer()
#         analysis = analyzer.get_analysis()
#         for analysis_name in self.EXPECTED_ANALYSES:
#             self.assertIn(analysis_name, analysis)
#
#     def test_save(self):
#         analyzer = self.get_link_analyzer()
#         output_path = analyzer.save(TEST_OUTPUT_DIR)
#         output_dict = JsonUtil.read_json_file(output_path)
#         self.assertIn(analyzer.ARTIFACT_TOKENS, output_dict)
#         self.assertIn(analyzer.ANALYSIS, output_dict)
#         for analysis in self.EXPECTED_ANALYSES:
#             self.assertIn(analysis, output_dict[analyzer.ANALYSIS])
#
#     def test_get_words_in_common(self):
#         expected_words_in_common = {"really", "body"}
#         analyzer = self.get_link_analyzer()
#         self.assertSetEqual(analyzer.get_words_in_common(), expected_words_in_common)
#
#     def test_get_misspelled_words(self):
#         analyzer = self.get_link_analyzer()
#         misspelled = analyzer.get_misspelled_words()
#         self.assertDictEqual(misspelled, self.EXPECTED_MISSPELLED_WORDS)
#
#     def test_get_shared_synonyms_and_antonyms(self):
#         analyzer = self.get_link_analyzer()
#         shared_syns, shared_ants = analyzer.get_shared_synonyms_and_antonyms()
#         self.assertIn('test', shared_syns)
#         self.assertIn('try', shared_syns['test'])
#         self.assertIn("small", shared_ants)
#         self.assertIn('large', shared_ants['small'])
#
#     def test_get_oov_vocab(self):
#         analyzer = self.get_link_analyzer()
#         oov = analyzer.get_oov_words()
#         expected_oov_words = deepcopy(self.EXPECTED_OOV_WORDS)
#         expected_oov_words.update(self.EXPECTED_MISSPELLED_WORDS)
#         self.assertDictEqual(oov, expected_oov_words)
#
#     def test_get_artifact_vocab(self):
#         analyzer = self.get_link_analyzer()
#         artifact = analyzer.link.source
#         vocab = analyzer.get_artifact_vocab(artifact)
#         expected_vocab = self.a1_body[:-1].lower().split()
#         TestAssertions.assert_lists_have_the_same_vals(self, vocab, expected_vocab)
#
#     def get_link_analyzer(self):
#         a1 = Artifact("s1", self.a1_body)
#         a2 = Artifact("t1", self.a2_body)
#         analyzer = LinkAnalyzer(TraceDataFrame(a1, a2, is_true_link=True), 0.66, ModelManager('bert-base-uncased'))
#         self.assertLessEqual(abs(analyzer.diff_from_prediction_score - 0.34), 0.01)
#         return analyzer
