import json
from copy import deepcopy

from typing import Dict, Union, List

from tgen.common.logging.logger_manager import logger
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.status import Status
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.relationship_manager.supported_relationship_managers import SupportedRelationshipManager
from tgen.tracing.ranking.filters.supported_filters import SupportedFilter
from tgen.tracing.ranking.selectors.selection_methods import SupportedSelectionMethod
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines


class RankingChunkJob(AbstractJob):
    """
    Uses large claude to rank all source artifacts.
    """
    MIN_THRESHOLD = 0.85

    def __init__(self, dataset_creator: PromptDatasetCreator = None, dataset: PromptDataset = None,
                 layer_ids: List[str] = None,
                 relationship_manager_type: SupportedRelationshipManager = SupportedRelationshipManager.EMBEDDING, **kwargs):
        """
        Uses dataset defined by role to sort and rank with big claude.
        :param dataset_creator: Creates the dataset to rank.
        :param artifact_df: DataFrame containing sources and targets.
        :param sorter: The sorting function to feed big claude with.
        :param layer_ids: The layers to rank between.
        :param ranking_pipeline: The pipeline used to rank children to each parent.
        """
        super().__init__()
        self.dataset_creator = dataset_creator
        self.dataset: PromptDataset = dataset
        self.layer_ids = layer_ids
        self.ranking_kwargs = kwargs
        self.relationship_manager_type = relationship_manager_type

    def _run(self, **kwargs) -> Union[Dict, AbstractTraceOutput]:
        """
        Sorts children artifacts then ranks them with big claude.
        :param kwargs: Additional keyword arguments.
        :return:
        """
        # ORIGINAL RANKING JOB
        logger.log_with_title("Starting regular ranking job.")
        base_ranking_kwargs = DictUtil.update_kwarg_values(
            self.ranking_kwargs, selection_method=SupportedSelectionMethod.SELECT_BY_THRESHOLD_NORMALIZED_CHILDREN,
            link_threshold=RankingChunkJob.MIN_THRESHOLD)
        base_ranking_job = self.create_ranking_job(relationship_manager=self.relationship_manager_type.value(),
                                                   **base_ranking_kwargs)
        base_results = base_ranking_job.run()

        with_filter_kwargs = DictUtil.update_kwarg_values(base_ranking_kwargs, filter=SupportedFilter.SIMILARITY_THRESHOLD)

        # RANKING WITH CHUNKS
        logger.log_with_title("Starting ranking job with Chunks.")
        chunk_ranking_job = self.create_ranking_job(use_chunks=True, relationship_manager=base_ranking_job.relationship_manager,
                                                    **with_filter_kwargs)
        chunk_results: JobResult = chunk_ranking_job.run()

        # TODO clean this up once we stop experimenting
        job_results = {"Chunks": chunk_results, "Base": base_results}

        for job_type, job_result in deepcopy(job_results).items():
            if job_result.status != Status.SUCCESS:
                logger.error(job_result.body)
                job_results.pop(job_type)

        if not job_results or "Chunks" not in job_results:
            raise Exception("Job has failed.")

        for job_type, job_result in job_results.items():
            tracing_results: TracePredictionOutput = job_result.body
            metrics = tracing_results.metrics
            if metrics:
                logger.log_with_title(f"Results for Tracing with {job_type}", json.dumps(metrics))

        return job_results["Chunks"].body

    def create_ranking_job(self, **kwargs) -> RankingJob:
        """
        Creates a ranking job with the given arguments.
        :param kwargs: Additional arguments to the job.
        :return: The ranking job.
        """
        return RankingJob(dataset_creator=self.dataset_creator, dataset=self.dataset, layer_ids=self.layer_ids,
                          ranking_pipeline=SupportedRankingPipelines.EMBEDDING, select_top_predictions=True,
                          log_results=False, **kwargs)
