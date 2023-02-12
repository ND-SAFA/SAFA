import os

from analysis.link_analyzer import LinkAnalyzer
from analysis.results_analyzer import ResultsAnalyzer
from data.datasets.trace_dataset import TraceDataset
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from testres.base_trace_test import BaseTraceTest
from testres.paths.paths import TEST_OUTPUT_DIR
from testres.test_assertions import TestAssertions
from train.trace_output.trace_prediction_output import TracePredictionOutput
from util.json_util import JsonUtil


class TestResultsAnalyzer(BaseTraceTest):
    a1_body = "This is a really small artifact body to use as a test."
    a2_body = "This is a really large artifct body to try out for funsies."
    a3_body = "Another 1.0 from Betito just for funsies and stuff!"
    a4_body = "Yet another because I need to write stuff for this test."

    A1 = Artifact("s1", a1_body)
    A2 = Artifact("t1", a2_body)
    A3 = Artifact("t2", a3_body)
    A4 = Artifact("s2", a4_body)

    ALL_LINKS = [TraceLink(A1, A2, True), TraceLink(A1, A3, False), TraceLink(A4, A2, False), TraceLink(A4, A3, True)]

    EXPECTED_CATEGORIZATIONS = {ALL_LINKS[0].id: [LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS],
                                ALL_LINKS[1].id: [],
                                ALL_LINKS[2].id: [LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS],
                                ALL_LINKS[3].id: [LinkAnalyzer.COMMON_WORDS]}
    MIS_PREDICTED_LINKS = ALL_LINKS[:2]
    CORRECTLY_PREDICTED_LINKS = ALL_LINKS[2:]

    def test_analyze_and_save(self):
        analyzer = self.get_results_analyzer()
        save_path = analyzer.analyze_and_save(TEST_OUTPUT_DIR, save_link_analysis=True, common_words_threshold=0.2)
        output = JsonUtil.read_json_file(save_path)
        self.assertIn(analyzer.MIS_PREDICTED_LINK_CATEGORIZATIONS, output)
        self.assertIn(analyzer.MIS_PREDICTED_N_PER_CATEGORY, output)
        self.assertIn(analyzer.CORRECTLY_PREDICTED_N_PER_CATEGORY, output)

        def add_to_expected_n_per_category(link_id, expected_n_per_category):
            for cat in self.EXPECTED_CATEGORIZATIONS[link_id]:
                if cat not in expected_n_per_category:
                    expected_n_per_category[cat] = 0
                expected_n_per_category[cat] = + 1

        mis_predicted_expected_n_per_category = {LinkAnalyzer.MISSPELLED_WORDS: 2, LinkAnalyzer.OOV_WORDS: 2}
        for link in self.MIS_PREDICTED_LINKS:
            self.assertIn(str(link.id), output[analyzer.MIS_PREDICTED_LINK_CATEGORIZATIONS])
            add_to_expected_n_per_category(link.id, mis_predicted_expected_n_per_category)
        self.assertDictEqual(mis_predicted_expected_n_per_category, output[analyzer.MIS_PREDICTED_N_PER_CATEGORY])

        correctly_predicted_expected_n_per_category = {LinkAnalyzer.MISSPELLED_WORDS: 2, LinkAnalyzer.OOV_WORDS: 2}
        for link in self.CORRECTLY_PREDICTED_LINKS:
            add_to_expected_n_per_category(link.id, correctly_predicted_expected_n_per_category)
        self.assertDictEqual(correctly_predicted_expected_n_per_category, output[analyzer.CORRECTLY_PREDICTED_N_PER_CATEGORY])

        output_files = os.listdir(TEST_OUTPUT_DIR)
        for link in analyzer.mis_predicted_links:
            self.assertIn(LinkAnalyzer.OUTPUT_FILENAME.format(link.id), output_files)

    def test_get_n_per_category(self):
        analyzer = self.get_results_analyzer()
        expected_n_per_category = {LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS: 2, LinkAnalyzer.COMMON_WORDS: 1,
                                   LinkAnalyzer.OOV_WORDS: 4, LinkAnalyzer.MISSPELLED_WORDS: 4}
        categorizations = {link_id: categories + [LinkAnalyzer.MISSPELLED_WORDS, LinkAnalyzer.OOV_WORDS]
                           for link_id, categories in self.EXPECTED_CATEGORIZATIONS.items()}
        n_per_category = analyzer._get_n_per_category(categorizations)
        self.assertDictEqual(expected_n_per_category, n_per_category)

    def test_analyze_links(self):
        analyzer = self.get_results_analyzer()
        link_categorizations = analyzer._analyze_links(links=set(self.ALL_LINKS), common_words_threshold=0.2)
        self.assertEquals(len(link_categorizations), len(self.ALL_LINKS))
        for link_id, categories in link_categorizations.items():
            expected_categories = self.EXPECTED_CATEGORIZATIONS[link_id] + [LinkAnalyzer.MISSPELLED_WORDS, LinkAnalyzer.OOV_WORDS]
            TestAssertions.assert_lists_have_the_same_vals(self, expected_categories, categories)

    def test_get_mis_and_correctly_predicted_links(self):
        analyzer = self.get_results_analyzer()
        TestAssertions.assert_lists_have_the_same_vals(self, analyzer.mis_predicted_links, self.MIS_PREDICTED_LINKS)
        TestAssertions.assert_lists_have_the_same_vals(self, analyzer.correctly_predicted_links, self.CORRECTLY_PREDICTED_LINKS)

    def get_results_analyzer(self):
        model_manager = ModelManager('bert-base-uncased')

        links = {link.id: link for link in self.ALL_LINKS}
        eval_dataset = TraceDataset(links, pos_link_ids=[link.id for link in self.ALL_LINKS if link.is_true_link],
                                    neg_link_ids=[link.id for link in self.ALL_LINKS if not link.is_true_link])
        label_ids = []
        for i, link in enumerate(eval_dataset.get_ordered_links()):
            if link in self.MIS_PREDICTED_LINKS:
                label_ids.append(abs(link.get_label()-1))
            elif link in self.CORRECTLY_PREDICTED_LINKS:
                label_ids.append(link.get_label())

        prediction_output = TracePredictionOutput(source_target_pairs=eval_dataset.get_source_target_pairs(),
                                                  label_ids=label_ids)
        return ResultsAnalyzer(prediction_output, eval_dataset, model_manager)
