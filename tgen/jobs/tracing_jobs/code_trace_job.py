import os

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from tgen.jobs.abstract_job import AbstractJob
from tgen.tracing.code_tracer import CodeTracer


class TraceCodeJob(AbstractJob):
    def __init__(self, dataset_creator: TraceDatasetCreator, export_dir: str,
                 format_type: SupportedDatasetExporter = SupportedDatasetExporter.DF):
        super().__init__()
        self.dataset_creator = dataset_creator
        self.export_dir = export_dir
        self.format_type = format_type

    def _run(self):
        trace_dataset = self.dataset_creator.create()
        code_tracer = CodeTracer(trace_dataset)
        code_tracer.trace()

        df_export_path = os.path.join(self.export_dir, "df-export")
        df_exporter = DataFrameExporter(df_export_path, dataset=trace_dataset)
        df_exporter.export()

        safa_export_path = os.path.join(self.export_dir, "safa-export")
        safa_exporter = SafaExporter(safa_export_path, dataset=trace_dataset)
        safa_exporter.export()
