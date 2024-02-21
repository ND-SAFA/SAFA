from typing import Any

from tgen.common.util.dict_util import DictUtil
from tgen.common.util.file_util import FileUtil
from tgen.contradictions.contradictions_detector import ContradictionsDetector
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class ContradictionJob(AbstractJob):

    def __init__(self, dataset_creator: TraceDatasetCreator, export_dir: str = None, job_args: JobArgs = None):
        """
        Initializes the job to detect contradictions in requirements.
        :param dataset_creator: Creates the dataset containing the requirements.
        :param job_args: The arguments need for the job.
        """
        self.trace_dataset_creator = dataset_creator
        self.export_dir = export_dir
        FileUtil.create_dir_safely(self.export_dir)
        super().__init__(job_args)

    def _run(self) -> Any:
        """
        Runs the job to detect duplicates.
        :return:
        """
        dataset = self.trace_dataset_creator.create()
        detector = ContradictionsDetector(dataset, export_path=self.export_dir)
        contradictions = detector.detect()
        predicted_contradictions = {link_id for c, link_ids in contradictions.items() for link_id in link_ids}
        predictions = [DictUtil.update_kwarg_values(dataset.trace_df.get_link(link_id), score=int(link_id in predicted_contradictions))
                       for link_id in dataset.trace_df.index]
        if len(dataset.trace_df.get_links_with_label(1)) > 0:
            RankingUtil.evaluate_trace_predictions(dataset.trace_df, predictions)
