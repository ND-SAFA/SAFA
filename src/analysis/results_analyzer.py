import os
from typing import List, Dict, Any, Set, Tuple

from tqdm import tqdm

from analysis.link_analyzer import LinkAnalyzer
from constants import LINK_COMMON_WORDS_THRESHOLD_DEFAULT, SAVE_LINK_ANALYSIS_DEFAULT
from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from train.trace_output.trace_prediction_output import TracePredictionOutput
from util.file_util import FileUtil
from util.json_util import JsonUtil

LINK_CATEGORIZATIONS = Dict[int, List[str]]


class ResultsAnalyzer:
    """
     Handles analysis of a trace link
     """

    MIS_PREDICTED_LINK_CATEGORIZATIONS = "mis_predicted_link_categorizations"
    MIS_PREDICTED_N_PER_CATEGORY = "mis_predicted_n_per_category"
    CORRECTLY_PREDICTED_N_PER_CATEGORY = "correctly_predicted_n_per_category"
    OUTPUT_FILENAME = "results_analysis.json"

    def __init__(self, prediction_output: TracePredictionOutput, dataset: TraceDataset, model_manager: ModelManager):
        """
        Initializes the analyzer for analysis of given prediction results
        :param prediction_output: The output of a prediction job
        :param dataset: The dataset associated with the result
        :param model_manager: The model to use to compare vocabs
        """
        self.prediction_output = prediction_output
        self.model_manager = model_manager
        self.mis_predicted_links, self.correctly_predicted_links = self._get_mis_and_correctly_predicted_links(dataset)

    def analyze_and_save(self, output_dir: str, save_link_analysis: bool = SAVE_LINK_ANALYSIS_DEFAULT,
                         common_words_threshold: float = LINK_COMMON_WORDS_THRESHOLD_DEFAULT) -> str:
        """
        Analyzes and saves the results of the prediction
        :param output_dir: The directory to output the results to
        :param save_link_analysis: If True, saves each individual link analysis
        :param common_words_threshold: % of total artifact words, above which link counts as sharing common words b/w artifacts
        :return: The path where the results were saved
        """
        mis_predicted_link_categorizations = self._analyze_links(links=self.mis_predicted_links,
                                                                 output_dir=output_dir if save_link_analysis else None,
                                                                 common_words_threshold=common_words_threshold)
        mis_predicted_n_per_category = self._get_n_per_category(mis_predicted_link_categorizations)
        correctly_predicted_link_categorizations = self._analyze_links(links=self.correctly_predicted_links,
                                                                       common_words_threshold=common_words_threshold)
        correct_n_per_category = self._get_n_per_category(correctly_predicted_link_categorizations)

        analysis = {self.MIS_PREDICTED_LINK_CATEGORIZATIONS: mis_predicted_link_categorizations,
                    self.MIS_PREDICTED_N_PER_CATEGORY: mis_predicted_n_per_category,
                    self.CORRECTLY_PREDICTED_N_PER_CATEGORY: correct_n_per_category
                    }
        return self._save(analysis, output_dir)

    def intersection(self, other: "ResultsAnalyzer") -> Set[TraceLink]:
        """
        Returns the intersection of mis-predicted links between self and other
        :param other: Another results analyzer
        :return: The set of overlapping mis-predicted links
        """
        return self.mis_predicted_links.intersection(other.mis_predicted_links)

    @staticmethod
    def _save(analysis: Dict[str, Any], output_dir: str) -> str:
        """
        Saves the results from the analysis
        :param output_dir: The directory to output the results to
        :return: The path where results were saved to
        """
        output = JsonUtil.dict_to_json(analysis)
        filepath = os.path.join(output_dir, ResultsAnalyzer.OUTPUT_FILENAME)
        FileUtil.write(output, filepath)
        return filepath

    @staticmethod
    def _get_n_per_category(link_categorizations: LINK_CATEGORIZATIONS) -> Dict[str, int]:
        """
        Gets the counts for each category that the mis-predicted links fall into
        :param link_categorizations: Dictionary mapping link id to the categories it falls into
        :return: A dictionary mapping category to the number of links in that category
        """
        n_per_category = {}
        for link, categories in link_categorizations.items():
            for category in categories:
                if category not in n_per_category:
                    n_per_category[category] = 0
                n_per_category[category] += 1
        return n_per_category

    def _analyze_links(self, links: Set[TraceLink], common_words_threshold: float, output_dir: str = None) -> LINK_CATEGORIZATIONS:
        """
        Analyzes all mis predicted links
        :param links: links to analyze
        :param common_words_threshold: % of total artifact words, above which link counts as sharing common words b/w artifacts
        :param output_dir: If provided saves the output if the link analysis to the directory
        :return: A dictionary mapping link id to the category it falls into
        """
        link_categorizations = {}
        for link in tqdm(links):
            link_categorizations[link.id] = []
            analyzer = LinkAnalyzer(link, self.model_manager)
            analysis_counts = analyzer.get_analysis_counts()
            total_words = sum([wc.total() for wc in analyzer.word_counts])
            shares_common_words = analysis_counts.pop(LinkAnalyzer.COMMON_WORDS) >= total_words * common_words_threshold
            if shares_common_words:
                link_categorizations[link.id].append(LinkAnalyzer.COMMON_WORDS)
            for analysis, count in analysis_counts.items():
                if count > 0:
                    link_categorizations[link.id].append(analysis)
            if output_dir:
                analyzer.save(output_dir)
        return link_categorizations

    def _get_mis_and_correctly_predicted_links(self, dataset: TraceDataset) -> Tuple[Set[TraceLink], Set[TraceLink]]:
        """
        Gets all mis and correctly predicted links from the output
        :param dataset: The dataset containing the original links
        :return: A set of the mis-predicted links and a set of the correctly predicted links
        """
        mis_predicted_links = set()
        correctly_predicted_links = set()
        for i, (source_id, target_id) in enumerate(self.prediction_output.source_target_pairs):
            link = dataset.links[TraceLink.generate_link_id(source_id, target_id)]
            pred_label = self.prediction_output.label_ids[i]
            if pred_label != link.get_label():
                mis_predicted_links.add(link)
            else:
                correctly_predicted_links.add(link)
        return mis_predicted_links, correctly_predicted_links
