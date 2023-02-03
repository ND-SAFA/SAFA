import os
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

import numpy as np

from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink
from train.metrics.metrics_manager import MetricsManager
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.logging.logger_manager import logger


@dataclass
class EpochTrainingResult:
    """
    Represents the Results of the Link Tracker for an Epoch
    """
    epoch_link_id_to_loss: Dict[int, float]
    pos_link_ids_worst_to_best: List[int]
    neg_link_ids_worst_to_best: List[int]
    POS_LINKS_KEY = "pos_links"
    NEG_LINKS_KEY = "neg_links"
    BEST_KEY = "best"
    WORST_KEY = "worst"


class LinkTrainingTracker:
    SAVE_TOP_N = 5
    SAVE_DIR = "link_tracking"
    SAVE_FILENAME = "result.json"

    def __init__(self, dataset: TraceDataset):
        """
        Handles tracking of individual losses for links
        :param dataset: The dataset used for training
        """
        self.dataset = dataset
        self.ordered_links = dataset.get_ordered_links()
        self._link_id_to_epoch_logits: Dict[int, List[float]] = {}
        self._training_results_for_epochs: List[EpochTrainingResult] = []

    def track_batch(self, batch_indices: List[int], batch_logits: List[List[float]]) -> None:
        """
        Tracks the results for each link in a batch
        :param batch_indices: The indices of the batch corresponding to links in the dataset
        :param batch_logits: The logits for each link in the batch
        :return: None
        """
        for i, logits in zip(batch_indices, batch_logits):
            link = self.ordered_links[i]
            self._link_id_to_epoch_logits[link.id] = logits

    def eval_last_epoch(self, save_path: str = None) -> Optional[EpochTrainingResult]:
        """
        Evaluates the last epoch and optionally saves the results
        :param save_path: The path to save to if desired
        :return: The results of the epoch
        """
        if not self._link_id_to_epoch_logits:
            return self.get_epoch_training_result(self.get_last_epoch_num())
        epoch_link_losses = self._calculate_epoch_link_losses()
        epoch_result = EpochTrainingResult(epoch_link_losses, *self._sort_link_ids_from_worst_to_best(epoch_link_losses))
        self._training_results_for_epochs.append(epoch_result)
        if save_path is not None:
            self.save_epoch_result(save_path, self.get_last_epoch_num())
        self._link_id_to_epoch_logits = {}
        return epoch_result

    def save_epoch_result(self, output_dir: str, epoch_iteration: int) -> bool:
        """
        Saves the results from an epoch
        :param output_dir: The base directory to save to
        :param epoch_iteration: The epoch iteration to save
        :return: True if successful, else False
        """
        epoch_result = self.get_epoch_training_result(epoch_iteration)
        if epoch_result is None:
            logger.warning("Cannot save until epoch %d has been evaluated" % epoch_iteration)
            return False
        output_dict = {EpochTrainingResult.POS_LINKS_KEY: self._get_worst_and_best_result(epoch_result.pos_link_ids_worst_to_best),
                       EpochTrainingResult.NEG_LINKS_KEY: self._get_worst_and_best_result(epoch_result.neg_link_ids_worst_to_best)}
        output_path = self.get_output_path(output_dir, epoch_iteration)
        output_json = JsonUtil.dict_to_json(output_dict)
        FileUtil.save_to_file(output_json, output_file_path=output_path)
        return True

    def get_output_path(self, output_dir: str, epoch_iteration: int) -> str:
        """
        Gets the path where output will be saved to
        :param output_dir: The base directory to save to
        :param epoch_iteration: The epoch iteration to save
        :return: The path to the output
        """
        return os.path.join(output_dir, self.SAVE_DIR, str(epoch_iteration), self.SAVE_FILENAME)

    def get_link_by_id(self, link_id: int) -> TraceLink:
        """
        Gets a TraceLink by its ID
        :param link_id: The ID of the TraceLink
        :return: The TrackLink
        """
        return self.dataset.links[link_id]

    def get_epoch_training_result(self, epoch_iteration: int = None) -> EpochTrainingResult:
        """
        Gets the results of an epoch
        :param epoch_iteration: The epoch iteration number to get results for
        :return: The EpochTrainingResult corresponding to the epoch iteration
        """
        epoch_iteration = self.get_last_epoch_num() if epoch_iteration is None else epoch_iteration
        if 0 <= epoch_iteration < len(self._training_results_for_epochs):
            return self._training_results_for_epochs[epoch_iteration]

    def get_last_epoch_num(self) -> int:
        """
        Gets the number of the last evaluated epoch
        :return: The iteration number of the last evaluated epoch
        """
        return len(self._training_results_for_epochs) - 1

    def _get_worst_and_best_result(self, worst_to_best_link_ids: List[int]) -> Dict[str, List[Tuple]]:
        """
        Gets a dictionary representing the worst and best links from the given list
        :param worst_to_best_link_ids: A ranked list of link_ids from worst (highest loss) to best (lowest loss)
        :return: a dictionary representing the worst and best links from the given list
        """
        worst_to_best_source_target = self.dataset.get_source_target_pairs(worst_to_best_link_ids)
        return {EpochTrainingResult.BEST_KEY: worst_to_best_source_target[-self.SAVE_TOP_N:],
                EpochTrainingResult.WORST_KEY: worst_to_best_source_target[:self.SAVE_TOP_N]}

    def _sort_link_ids_from_worst_to_best(self, epoch_link_losses: Dict[int, float]) -> Tuple[List[int], List[int]]:
        """
        Sorts the link ids from worst (highest loss) to best (lowest loss)
        :param epoch_link_losses: The dictionary mapping link id to its loss for the epoch
        :return: The ranked positive and negative link_ids
        """
        link_ids_worst_to_best = sorted(epoch_link_losses, key=epoch_link_losses.get, reverse=True)
        pos_link_ids_worst_to_best = []
        neg_link_ids_worst_to_best = []
        for link_id in link_ids_worst_to_best:
            if self.get_link_by_id(link_id).is_true_link:
                pos_link_ids_worst_to_best.append(link_id)
            else:
                neg_link_ids_worst_to_best.append(link_id)
        return pos_link_ids_worst_to_best, neg_link_ids_worst_to_best

    def _calculate_epoch_link_losses(self) -> Dict[int, float]:
        """
        Calculates the losses for each link in the epoch
        :return: A dictionary mapping link id to its loss for the epoch
        """
        epoch_link_losses = {}
        similarity_scores = MetricsManager.get_similarity_scores(np.asarray(list(self._link_id_to_epoch_logits.values())))
        for i, link_id in enumerate(self._link_id_to_epoch_logits.keys()):
            link = self.get_link_by_id(link_id)
            epoch_link_losses[link_id] = self._calculate_loss(link, similarity_scores[i])
        return epoch_link_losses

    @staticmethod
    def _calculate_loss(link: TraceLink, sim_score: float) -> float:
        """
        Calculates the link's loss for an epoch
        :param link: The TraceLink
        :param sim_score: The similarity score associated with the given link for an epoch
        :return: The link's loss
        """
        return abs(link.get_label() - sim_score)
