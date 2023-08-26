from enum import Enum

from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.exporters.safa_exporter import SafaExporter


class SupportedDatasetExporter(Enum):
    SAFA = SafaExporter
    CSV = CSVExporter
    DF = DataFrameExporter
