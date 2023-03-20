from data.exporters.abstract_dataset_exporter import AbstractDatasetExporter


class CSVExporter(AbstractDatasetExporter):

    def export(self) -> None:
        """
        Exports entities as a project in a CSV format.
        :return: None
        """
        df = self.get_dataset().to_dataframe()
        df.to_csv(self.export_path, index=False)
