from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager


class HGenJob(AbstractJob):

    def __init__(self, hgen_args: HGenArgs, llm_manager: AbstractLLMManager,
                 export_path: str = None, job_args: JobArgs = None):
        """
        Initializes the job with args needed for hierarchy generator
        :param hgen_args: The arguments required for the hierarchy generation
        :param llm_manager: Model Manager in charge of generating artifacts
        :param export_path: The path to which the final dataset will be exported
        :pram job_args: The arguments need for the job
        """
        self.hgen_args = hgen_args
        self.llm_manager = llm_manager
        self.export_path = export_path
        self.hgen = HierarchyGenerator(self.hgen_args, self.llm_manager)
        super().__init__(job_args)

    def _run(self) -> JobResult:
        """
        Runs the hierarchy generator and exports the resulting dataset
        :return: The result of the job
        """
        generated_dataset = self.hgen.run(export_path=self.export_path)
        return JobResult({JobResult.DATASET: generated_dataset})
