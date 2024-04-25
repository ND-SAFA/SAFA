import json
from copy import deepcopy
from typing import Dict, Union, List

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.logging.logger_manager import logger
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.file_util import FileUtil
from tgen.common.util.status import Status
from tgen.core.trace_output.abstract_trace_output import AbstractTraceOutput
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.relationship_manager.supported_relationship_managers import SupportedRelationshipManager
from tgen.tracing.ranking.filters.supported_filters import SupportedFilter
from tgen.tracing.ranking.selectors.selection_methods import SupportedSelectionMethod
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines

ResultType = Any


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
        export_dir = DictUtil.get_kwarg_values(self.ranking_kwargs, pop=True, export_dir=EMPTY_STRING)
        base_export_dir = FileUtil.safely_join_paths(export_dir, "base")
        base_ranking_kwargs = DictUtil.update_kwarg_values(
            self.ranking_kwargs, selection_method=SupportedSelectionMethod.SELECT_BY_THRESHOLD_SCALED,
            link_threshold=RankingChunkJob.MIN_THRESHOLD, export_dir=base_export_dir)
        base_ranking_job = self.create_ranking_job(relationship_manager=self.relationship_manager_type.value(),
                                                   **base_ranking_kwargs)
        base_results = base_ranking_job.run()

        chunk_export_dir = FileUtil.safely_join_paths(export_dir, "chunks")
        with_filter_kwargs = DictUtil.update_kwarg_values(base_ranking_kwargs, filter=SupportedFilter.SIMILARITY_THRESHOLD,
                                                          export_dir=chunk_export_dir)

        # RANKING WITH CHUNKS
        logger.log_with_title("Starting ranking job with Chunks.")
        chunk_ranking_job = self.create_ranking_job(use_chunks=True, relationship_manager=base_ranking_job.relationship_manager,
                                                    **with_filter_kwargs)
        chunk_results: JobResult = chunk_ranking_job.run()

        # TODO clean this up once we stop experimenting
        job_results = {"Chunks": chunk_results, "Base": base_results}

        self._display_results(job_results)

        return job_results["Chunks"].body

    def _perform_base_ranking(self):
        """
        Performs artifact ranking based on content.
        :return: Ranking Job, Ranking Kwargs, and Ranking Results.
        """
        logger.log_with_title("Starting regular ranking job.")
        base_ranking_kwargs = DictUtil.update_kwarg_values(
            self.ranking_kwargs,
            selection_method=SupportedSelectionMethod.SELECT_BY_THRESHOLD_NORMALIZED_CHILDREN,
            link_threshold=RankingChunkJob.MIN_THRESHOLD
        )
        base_ranking_job = self.create_ranking_job(**base_ranking_kwargs)
        base_results = base_ranking_job.run()
        return base_ranking_job, base_ranking_kwargs, base_results

    def _perform_chunk_ranking(self, embeddings_manager: EmbeddingsManager, with_filter_kwargs) -> TracePredictionOutput:
        """
        Performs ranking based on chunk algorithm.
        :param embeddings_manager: Embeddings manager with cached embeddings.
        :param with_filter_kwargs: Additional arguments to chunk ranking job.
        :return: Chunk results.
        """
        logger.log_with_title("Starting ranking job with Chunks.")
        chunk_ranking_job = self.create_ranking_job(use_chunks=True, embeddings_manager=embeddings_manager, **with_filter_kwargs)
        chunk_results: JobResult = chunk_ranking_job.run()
        return chunk_results

    def create_ranking_job(self, **kwargs) -> RankingJob:
        """
        Creates a ranking job with the given arguments.
        :param kwargs: Additional arguments to the job.
        :return: The ranking job.
        """
        return RankingJob(dataset_creator=self.dataset_creator, dataset=self.dataset, layer_ids=self.layer_ids,
                          ranking_pipeline=SupportedRankingPipelines.EMBEDDING, select_top_predictions=True,
                          log_results=False, **kwargs)

    def on_job_failure(self, save_path: str) -> None:
        """
        Overrides default failure behavior and saves state if job failed.
        :param save_path: The path to save state to.
        :return: None
        """
        super().on_job_failure(save_path)
        self.current_job.hgen.state.export_dir = save_path
        step_name = self.current_job.hgen.state.current_step
        self.current_job.hgen.state.save(step_name.lower())
        logger.info(f"Saved state to:{save_path}")

    @staticmethod
    def _display_results(job_results: Dict[str, ResultType]) -> None:
        """
        Prints ranking results to screen.
        :param job_results: The results to print.
        :return:None
        """
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
