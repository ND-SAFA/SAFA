from enum import Enum

from data.exporters.safa_exporter import SafaExporter


class SupportedExporters(Enum):
    SAFA = SafaExporter
