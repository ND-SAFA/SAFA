from typing import List

from analysis.link_analyzer import LinkAnalyzer
from analysis.results_analyzer import ResultsAnalyzer
from data.datasets.trace_dataset import TraceDataset
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from scripts.modules.analysis_types import JobAnalysis, LinkCollectionAnalysis, LinkMetrics
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions
from train.trace_output.trace_prediction_output import TracePredictionOutput


class TestResultsAnalyzer(BaseTraceTest):
    a1_body = "This is a really small artifact body to use as a test rationally."
    a2_body = "This is a really large artifct body to try out for funsies."
    a3_body = "Another 1.0 from Betito just for funsies and stuff!"
    a4_body = "Yet another because I need to write stuff for this test."

    A1 = Artifact("s1", a1_body)
    A2 = Artifact("t1", a2_body)
    A3 = Artifact("t2", a3_body)
    A4 = Artifact("s2", a4_body)

    ALL_LINKS = [TraceLink(A1, A2, True), TraceLink(A1, A3, False), TraceLink(A4, A2, False), TraceLink(A4, A3, True)]

    EXPECTED_CATEGORIZATIONS = {ALL_LINKS[0].id: [LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS, LinkAnalyzer.OOV_WORDS],
                                ALL_LINKS[1].id: [LinkAnalyzer.OOV_WORDS],
                                ALL_LINKS[2].id: [LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS],
                                ALL_LINKS[3].id: [LinkAnalyzer.COMMON_WORDS]}
    MIS_PREDICTED_LINKS = ALL_LINKS[:2]
    CORRECTLY_PREDICTED_LINKS = ALL_LINKS[2:]
    FALSE_NEGATIVE = ALL_LINKS[0]
    FALSE_POSITIVE = ALL_LINKS[1]

    def test_intersection(self):
        analyzer1 = self.get_results_analyzer()
        analyzer2 = self.get_results_analyzer(mis_predicted_links=[self.ALL_LINKS[0], self.ALL_LINKS[-1]])
        intersection = analyzer1.mis_predictions_intersection(analyzer2)
        self.assertEquals(len(intersection), 1)
        self.assertEquals(self.ALL_LINKS[0].id, intersection.pop())

    def test_analyze_and_save(self):
        analyzer = self.get_results_analyzer()
        job_analysis: JobAnalysis = analyzer.analyze(common_words_threshold=0.2)
        for mis_prediction_collection_name in ["false_positive_collection", "false_negative_collection"]:
            for link_id, link_analysis in job_analysis[mis_prediction_collection_name].items():
                self.assertIn("categories", link_analysis)
        self.assertIn("false_positive_n_per_category", job_analysis["summary"])
        self.assertIn("false_negative_n_per_category", job_analysis["summary"])
        self.assertIn("correctly_predicted_n_per_category", job_analysis["summary"])

        def add_to_expected_n_per_category(link_id, expected_n_per_category):
            for cat in self.EXPECTED_CATEGORIZATIONS[link_id]:
                if cat not in expected_n_per_category:
                    expected_n_per_category[cat] = 0
                expected_n_per_category[cat] += 1

        false_negative_expected_n_per_category = {LinkAnalyzer.MISSPELLED_WORDS: 1}
        false_positive_expected_n_per_category = {LinkAnalyzer.MISSPELLED_WORDS: 1}
        for link in self.MIS_PREDICTED_LINKS:
            if link.is_true_link:
                self.assertIn(link.id, job_analysis["false_negative_collection"].keys())
                add_to_expected_n_per_category(link.id, false_negative_expected_n_per_category)
            else:
                self.assertIn(link.id, job_analysis["false_positive_collection"].keys())
                add_to_expected_n_per_category(link.id, false_positive_expected_n_per_category)
        self.assertDictEqual(false_positive_expected_n_per_category, job_analysis["summary"]["false_positive_n_per_category"])
        self.assertDictEqual(false_negative_expected_n_per_category, job_analysis["summary"]["false_negative_n_per_category"])

        correctly_predicted_expected_n_per_category = {LinkAnalyzer.MISSPELLED_WORDS: 2}
        for link in self.CORRECTLY_PREDICTED_LINKS:
            add_to_expected_n_per_category(link.id, correctly_predicted_expected_n_per_category)
        self.assertDictEqual(correctly_predicted_expected_n_per_category,
                             job_analysis["summary"]["correctly_predicted_n_per_category"])

    def test_get_n_per_category(self):
        analyzer = self.get_results_analyzer()
        expected_n_per_category = {LinkAnalyzer.SHARED_SYNONYMS_AND_ANTONYMS: 2, LinkAnalyzer.COMMON_WORDS: 1,
                                   LinkAnalyzer.OOV_WORDS: 2, LinkAnalyzer.MISSPELLED_WORDS: 4}
        categorizations: LinkCollectionAnalysis = {
            link_id: LinkMetrics(categories=categories + [LinkAnalyzer.MISSPELLED_WORDS])
            for link_id, categories in self.EXPECTED_CATEGORIZATIONS.items()}
        n_per_category = analyzer._get_n_per_category(categorizations)
        self.assertDictEqual(expected_n_per_category, n_per_category)

    def test_analyze_links(self):
        analyzer = self.get_results_analyzer()
        link_categorizations = analyzer._analyze_link_collection(links=set(self.ALL_LINKS), common_words_threshold=0.2)
        self.assertEquals(len(link_categorizations), len(self.ALL_LINKS))
        for link_id, link_analysis in link_categorizations.items():
            expected_categories = self.EXPECTED_CATEGORIZATIONS[link_id] + [LinkAnalyzer.MISSPELLED_WORDS]
            TestAssertions.assert_lists_have_the_same_vals(self, expected_categories, link_analysis["categories"])

    def test_get_mis_and_correctly_predicted_links(self):
        analyzer = self.get_results_analyzer()
        TestAssertions.assert_lists_have_the_same_vals(self, analyzer.mis_predicted_links.false_positives, [self.FALSE_POSITIVE])
        TestAssertions.assert_lists_have_the_same_vals(self, analyzer.mis_predicted_links.false_negatives, [self.FALSE_NEGATIVE])
        TestAssertions.assert_lists_have_the_same_vals(self, analyzer.correctly_predicted_links, self.CORRECTLY_PREDICTED_LINKS)

    def get_results_analyzer(self, mis_predicted_links=None):
        model_manager = ModelManager('bert-base-uncased')

        links = {link.id: link for link in self.ALL_LINKS}
        eval_dataset = TraceDataset(links, pos_link_ids=[link.id for link in self.ALL_LINKS if link.is_true_link],
                                    neg_link_ids=[link.id for link in self.ALL_LINKS if not link.is_true_link])
        predictions = self.get_predictions(eval_dataset, mis_predicted_links=self.MIS_PREDICTED_LINKS if not mis_predicted_links
        else mis_predicted_links)

        prediction_output = TracePredictionOutput(source_target_pairs=eval_dataset.get_source_target_pairs(),
                                                  predictions=predictions)
        return ResultsAnalyzer(prediction_output, eval_dataset, model_manager)

    @staticmethod
    def get_predictions(dataset: TraceDataset, mis_predicted_links: List):
        predictions = []
        for i, link in enumerate(dataset.get_ordered_links()):
            if link in mis_predicted_links:
                predictions.append(abs(link.get_label() - 1))
            else:
                predictions.append(link.get_label())
        return predictions
