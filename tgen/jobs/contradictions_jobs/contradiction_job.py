from typing import Any

from tgen.common.util.dict_util import DictUtil
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.requirements_contradictions.contradictions_detector import ContradictionsDetector
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class ContradictionJob(AbstractJob):

    def __init__(self, trace_dataset_creator: TraceDatasetCreator, job_args: JobArgs = None):
        """
        Initializes the job to detect contradictions in requirements.
        :param trace_dataset_creator: Creates the dataset containing the requirements.
        :param job_args: The arguments need for the job.
        """
        self.trace_dataset_creator = trace_dataset_creator
        super().__init__(job_args)

    def _run(self) -> Any:
        """
        Runs the job to detect duplicates.
        :return:
        """
        dataset = self.trace_dataset_creator.create()
        detector = ContradictionsDetector(dataset)
        contradictions = detector.detect()
        predicted_contradictions = {link_id for c, link_ids in contradictions.items() for link_id in link_ids}
        predictions = [DictUtil.update_kwarg_values(dataset.trace_df.get_link(link_id), score=int(link_id in predicted_contradictions))
                       for link_id in dataset.trace_df.index]
        if len(dataset.trace_df.get_links_with_label(1)) > 0:
            RankingUtil.evaluate_trace_predictions(dataset.trace_df, predictions)
