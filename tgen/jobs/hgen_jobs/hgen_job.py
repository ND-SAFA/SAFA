from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult


class HGenJob(AbstractJob):

    def __init__(self, hgen_args: HGenArgs, export_path: str, save_on_each_step: bool = True, job_args: JobArgs = None):
        """
        Initializes the job with args needed for hierarchy generator
        :param hgen_args: The arguments required for the hierarchy generation
        :param export_path: The path to which the final dataset will be exported
        :param save_on_each_step: If True, saves the dataset on each step of the hierarchy generation
        :pram job_args: The arguments need for the job
        """
        self.hgen_args = hgen_args
        self.export_path = export_path
        self.save_on_each_step = save_on_each_step
        super().__init__(job_args)

    def _run(self) -> JobResult:
        """
        Runs the hierarchy generator and exports the resulting dataset
        :return: The result of the job
        """

        hgen = HierarchyGenerator(self.hgen_args)
        generated_dataset = hgen.run(export_path=self.export_path if self.save_on_each_step else None)
        exporter = CSVExporter(export_path=self.export_path, dataset=generated_dataset)
        exporter.export()
        return JobResult({JobResult.EXPORT_PATH: self.export_path})
