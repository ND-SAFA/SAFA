import os

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.jobs.abstract_job import AbstractJob
from tgen.tracing.code.code_tracer import CodeTracer


class TraceCodeJob(AbstractJob):
    def __init__(self, dataset_creator: TraceDatasetCreator, export_dir: str, add_packages: bool = True):
        """
        Creates code tracer for a defined dataset.
        :param dataset_creator: The creator used to generate the dataset.
        :param export_dir: The path to the directory to export dataset to.
        :param add_packages: Whether to add packages as artifacts.
        """
        super().__init__()
        self.dataset_creator = dataset_creator
        self.export_dir = export_dir
        self.add_packages = add_packages

    def _run(self):
        """
        Adds links between source code and optionally adds packages as artifacts.
        :return: None (datasets with changes are exported).
        """
        trace_dataset = self.dataset_creator.create()
        code_tracer = CodeTracer(trace_dataset)
        code_tracer.trace(add_packages=self.add_packages)

        if self.export_dir:
            df_export_path = os.path.join(self.export_dir, "df-export")
            df_exporter = DataFrameExporter(df_export_path, dataset=trace_dataset)
            df_exporter.export()

            safa_export_path = os.path.join(self.export_dir, "safa-export")
            safa_exporter = SafaExporter(safa_export_path, dataset=trace_dataset)
            safa_exporter.export()
