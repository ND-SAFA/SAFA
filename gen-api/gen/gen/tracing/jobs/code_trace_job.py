import os

from gen_common.util.file_util import FileUtil
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.exporters.dataframe_exporter import DataFrameExporter
from gen_common.data.exporters.safa_exporter import SafaExporter
from gen_common.jobs.abstract_job import AbstractJob
from gen.tracing.code.code_tracer import CodeTracer


class TraceCodeJob(AbstractJob):
    def __init__(self, dataset_creator: TraceDatasetCreator, export_dir: str, add_packages: bool = True,
                 extensions: str = None):
        """
        Creates code tracer for a defined dataset.
        :param dataset_creator: The creator used to generate the dataset.
        :param export_dir: The path to the directory to export dataset to.
        :param add_packages: Whether to add packages as artifacts.
        :param extensions: The file extensions to keep.
        """
        super().__init__()
        self.dataset_creator = dataset_creator
        self.export_dir = export_dir
        self.add_packages = add_packages
        self.extensions = extensions.split(",") if extensions else None

    def _run(self):
        """
        Adds links between source code and optionally adds packages as artifacts.
        :return: None (datasets with changes are exported).
        """
        trace_dataset = self.dataset_creator.create()
        if self.extensions:
            artifact_names = [f for f in trace_dataset.artifact_df.index
                              if FileUtil.get_file_ext(f) in self.extensions]
            trace_dataset.artifact_df = trace_dataset.artifact_df.filter_by_index(artifact_names)

        code_tracer = CodeTracer(trace_dataset)
        code_tracer.trace(add_packages=self.add_packages)

        if self.export_dir:
            df_export_path = os.path.join(self.export_dir, "df-export")
            df_exporter = DataFrameExporter(df_export_path, dataset=trace_dataset)
            df_exporter.export()

            safa_export_path = os.path.join(self.export_dir, "safa-export")
            safa_exporter = SafaExporter(safa_export_path, dataset=trace_dataset)
            safa_exporter.export()
