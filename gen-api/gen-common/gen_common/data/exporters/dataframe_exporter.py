import os

from gen_common.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from gen_common.data.keys.csv_keys import CSVKeys
from gen_common.infra.t_logging.logger_manager import logger


class DataFrameExporter(AbstractDatasetExporter):
    PROJECT_DATAFRAMES = ["artifact_df", "trace_df", "layer_df"]

    @staticmethod
    def include_filename() -> bool:
        """
        Export path should not include a filename
        :return: False
        """
        return False

    def export(self, **kwargs) -> None:
        """
        Exports the dataset as three dataframes (artifact, trace, layer)
        :param kwargs: Any additional parameters needed for export (unused)
        :return: None
        """
        dataset = self.get_dataset()
        for dataframe_name in self.PROJECT_DATAFRAMES:
            df = getattr(dataset, dataframe_name)
            df.to_csv(os.path.join(self.export_path, f"{dataframe_name}{CSVKeys.EXT}"))
        logger.info(f"Exported DataFrame dataset to {self.export_path}")
