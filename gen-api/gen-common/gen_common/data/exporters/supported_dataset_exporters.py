from enum import Enum

from gen_common.data.exporters.csv_exporter import CSVExporter
from gen_common.data.exporters.dataframe_exporter import DataFrameExporter
from gen_common.data.exporters.safa_exporter import SafaExporter


class SupportedDatasetExporter(Enum):
    SAFA = SafaExporter
    CSV = CSVExporter
    DF = DataFrameExporter
