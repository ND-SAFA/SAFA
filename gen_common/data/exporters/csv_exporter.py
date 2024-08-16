from gen_common.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter

from gen_common.infra.t_logging.logger_manager import logger


class CSVExporter(AbstractDatasetExporter):

    @staticmethod
    def include_filename() -> bool:
        """
        Returns True bc the dataset exporter expects the export path to include the filename
        :return: True
        """
        return True

    def export(self, include_index: bool = True, **kwargs) -> None:
        """
        Exports entities as a project in a CSV format.
        :param include_index: Whether to include index of data frame in export.
        :return: None
        """
        df = self.get_dataset().to_dataframe()
        df.to_csv(self.export_path, index=include_index)
        logger.info(f"Exported data frame to: {self.export_path}")
