from typing import List

from analysis.dataset_analyzer import DatasetAnalyzer
from data.creators.trace_dataset_creator import TraceDatasetCreator
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager


class AnalyzeDatasetJob(AbstractJob):

    def __init__(self, job_args: JobArgs, dataset_creator: TraceDatasetCreator, model_managers: List[ModelManager]):
        """
        Responsible for creating and saving new data
        :param job_args: the arguments for the job
        :param dataset_creator: creates the dataset to analyze
        :param model_managers: List of model managers to use to analyze OOV words
        """
        job_args.save_dataset_splits = True
        super().__init__(job_args=job_args)
        self.dataset_creator = dataset_creator
        self.model_managers = model_managers

    def _run(self, **kwargs) -> JobResult:
        """
        Creates and saves the data
        :return: job results including location of saved data
        """
        dataset = self.dataset_creator.create()
        analyzer = DatasetAnalyzer(dataset, self.model_managers)
        analyzer.analyze_and_save(self.job_args.output_dir)
        return JobResult()
