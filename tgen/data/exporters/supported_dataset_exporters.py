from enum import Enum

from data.exporters.csv_exporter import CSVExporter
from data.exporters.safa_exporter import SafaExporter


class SupportedDatasetExporter(Enum):
    SAFA = SafaExporter
    CSV = CSVExporter
