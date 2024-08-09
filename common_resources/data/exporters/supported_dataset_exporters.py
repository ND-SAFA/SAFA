from enum import Enum

from common_resources.data.exporters.csv_exporter import CSVExporter
from common_resources.data.exporters.dataframe_exporter import DataFrameExporter
from common_resources.data.exporters.safa_exporter import SafaExporter


class SupportedDatasetExporter(Enum):
    SAFA = SafaExporter
    CSV = CSVExporter
    DF = DataFrameExporter
