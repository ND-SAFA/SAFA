import os
from unittest.mock import patch

from data.tree.trace_link import TraceLink
from testres.base_trace_test import BaseTraceTest
from testres.paths.paths import TEST_OUTPUT_DIR
from train.trackers.link_training_tracker import EpochTrainingResult, LinkTrainingTracker
from util.json_util import JsonUtil


class TestLinkTrainingTracker(BaseTraceTest):
    BATCH_INDICES, BATCH_LOGITS = [2, 10, 5, 1], [[-0.00614631, - 0.01146667], [-0.01539335, - 0.01543014],
                                                  [-0.00492693, - 0.01589241], [-0.00748538, - 0.01545507]]
    DATASET = BaseTraceTest.get_trace_dataset()
    EXPECTED_SIM_SCORE = 0.5

    def test_track_batch_and_eval_epoch(self):
        tracker = self.get_link_training_tracker()
        tracker.track_batch(self.BATCH_INDICES, self.BATCH_LOGITS)
        ordered_links = self.DATASET.get_ordered_links()
        for i, batch_index in enumerate(self.BATCH_INDICES):
            link = ordered_links[batch_index]
            self.assertIn(link.id, tracker._link_id_to_epoch_logits)
            self.assertEquals(tracker._link_id_to_epoch_logits[link.id], self.BATCH_LOGITS[i])

    @patch.object(LinkTrainingTracker, "save_epoch_result")
    def test_eval_epoch(self, save_epoch_result_mock):
        tracker = self.get_link_training_tracker()
        tracker.track_batch(self.BATCH_INDICES, self.BATCH_LOGITS)
        tracker.eval_last_epoch(save_path=None)
        self.assertFalse(tracker._link_id_to_epoch_logits)
        self.assertEquals(len(tracker._training_results_for_epochs), 1)
        self.assertEquals(len(tracker.get_epoch_training_result().epoch_link_id_to_loss), len(self.BATCH_INDICES))
        self.assertFalse(save_epoch_result_mock.called)
        tracker.track_batch(self.BATCH_INDICES, self.BATCH_LOGITS)
        tracker.eval_last_epoch(save_path=TEST_OUTPUT_DIR)
        self.assertEquals(len(tracker._training_results_for_epochs), 2)
        self.assertEquals(len(tracker.get_epoch_training_result(1).epoch_link_id_to_loss), len(self.BATCH_INDICES))
        self.assertTrue(save_epoch_result_mock.called)

    def test_save_epoch_result(self):
        tracker = self.get_link_training_tracker()
        tracker.track_batch(self.BATCH_INDICES, self.BATCH_LOGITS)
        self.assertFalse(tracker.save_epoch_result(TEST_OUTPUT_DIR, 0))
        tracker.eval_last_epoch(save_path=None)
        self.assertTrue(tracker.save_epoch_result(TEST_OUTPUT_DIR, 0))
        output_path = tracker.get_output_path(TEST_OUTPUT_DIR, 0)
        self.assertTrue(os.path.exists(output_path))
        output_dict = JsonUtil.read_json_file(output_path)
        self.assertIn(EpochTrainingResult.POS_LINKS_KEY, output_dict)
        self.assertIn(EpochTrainingResult.NEG_LINKS_KEY, output_dict)

    @patch("data.tree.artifact.Artifact")
    def test_calculate_loss(self, mock_artifact):
        pos_link = TraceLink(mock_artifact, mock_artifact, is_true_link=True)
        self.assertEquals(.6, LinkTrainingTracker._calculate_loss(pos_link, .4))
        neg_link = TraceLink(mock_artifact, mock_artifact, is_true_link=False)
        self.assertEquals(.4, LinkTrainingTracker._calculate_loss(neg_link, .4))

    def test_calculate_epoch_losses(self):
        tracker = self.get_link_training_tracker()
        tracker.track_batch(self.BATCH_INDICES, self.BATCH_LOGITS)
        epoch_link_losses = tracker._calculate_epoch_link_losses()
        ordered_links = self.DATASET.get_ordered_links()
        for i, batch_index in enumerate(self.BATCH_INDICES):
            link = ordered_links[batch_index]
            self.assertIn(link.id, epoch_link_losses)
            self.assertLess(self.EXPECTED_SIM_SCORE - epoch_link_losses[link.id], 0.1)

    @patch("data.tree.artifact.Artifact")
    @patch.object(LinkTrainingTracker, "get_link_by_id")
    def test_sort_link_ids_from_worst_to_best(self, mock_get_link_by_id, mock_artifact):
        def is_true_link(link_id):
            if link_id % 2 == 0:
                return TraceLink(mock_artifact, mock_artifact, is_true_link=True)
            else:
                return TraceLink(mock_artifact, mock_artifact, is_true_link=False)

        mock_get_link_by_id.side_effect = is_true_link
        epoch_link_losses = {123: 0.5, 456: 0.4, 789: 0.6}
        expected_worst_to_best = [789, 123, 456]
        tracker = self.get_link_training_tracker()
        pos_links, neg_links = tracker._sort_link_ids_from_worst_to_best(epoch_link_losses)
        self.assertEquals(2, len(neg_links))
        self.assertEquals(1, len(pos_links))
        self.assertLess(expected_worst_to_best.index(neg_links[0]), expected_worst_to_best.index(neg_links[1]))

    def test_get_worst_and_best_result(self):
        test_worst_to_best = list(self.DATASET.links.keys())
        source_target = self.DATASET.get_source_target_pairs(test_worst_to_best)
        tracker = self.get_link_training_tracker()
        result = tracker._get_worst_and_best_result(test_worst_to_best)
        self.assertIn(EpochTrainingResult.WORST_KEY, result)
        self.assertListEqual(source_target[:tracker.SAVE_TOP_N], result[EpochTrainingResult.WORST_KEY])
        self.assertIn(EpochTrainingResult.BEST_KEY, result)
        self.assertListEqual(source_target[-tracker.SAVE_TOP_N:], result[EpochTrainingResult.BEST_KEY])

    def get_link_training_tracker(self):
        return LinkTrainingTracker(self.DATASET)
