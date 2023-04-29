from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter


class CSVExporter(AbstractDatasetExporter):

    @staticmethod
    def include_filename() -> bool:
        """
        Returns True if the dataset exporter expects the export path to include the filename, else False
        :return: True if the dataset exporter expects the export path to include the filename, else False
        """
        return True

    def export(self, include_index: bool = True, **kwargs) -> None:
        """
        Exports entities as a project in a CSV format.
        :return: None
        """
        df = self.get_dataset().to_dataframe()
        df.to_csv(self.export_path, index=include_index)
