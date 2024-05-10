from typing import Any

from tgen.common.util.dict_util import DictUtil
from tgen.contradictions.with_decision_tree.contradictions_detector_with_tree import ContradictionsDetectorWithTree
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class ContradictionJob(AbstractJob):

    def __init__(self, job_args: JobArgs = None):
        """
        Initializes the job to detect contradictions in requirements.
        :param job_args: The arguments need for the job.
        """
        super().__init__(job_args)

    def _run(self) -> Any:
        """
        Runs the job to detect duplicates.
        :return:
        """
        dataset = self.job_args.dataset
        detector = ContradictionsDetectorWithTree(dataset, export_path=self.job_args.export_dir)
        contradictions = detector.detect_all()
        predicted_contradictions = {link_id for c, link_ids in contradictions.items() for link_id in link_ids}
        predictions = [DictUtil.update_kwarg_values(dataset.trace_df.get_link(link_id), score=int(link_id in predicted_contradictions))
                       for link_id in dataset.trace_df.index]
        if len(dataset.trace_df.get_links_with_label(1)) > 0:
            RankingUtil.evaluate_trace_predictions(dataset.trace_df, predictions)
