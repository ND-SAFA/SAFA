from typing import Dict, List, Tuple, Union

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.server.api.api_definition import ApiDefinition
from tgen.util.json_util import JsonUtil


class ApiExporter(AbstractDatasetExporter):

    def __init__(self, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None, export_path: str = ''):
        """
        Initializes exporter for given trace dataset.
        :param dataset: The dataset to export
        :param dataset_creator: The creator in charge of making the dataset to export
        :param export_path: The path to export the dataset to
        """
        super().__init__(dataset_creator=dataset_creator, dataset=dataset, export_path=export_path)
        self.source_layers: Dict[str, Dict[str, str]] = {}
        self.target_layers: Dict[str, Dict[str, str]] = {}
        self.true_links: List[Tuple[str, str]] = []

    def export(self, **kwargs) -> ApiDefinition:
        """
        Exports the dataset to the ApiDefinition format
        :return: The ApiDefinition
        """
        dataset = self.get_dataset()
        self.true_links = dataset.get_source_target_pairs(dataset.get_pos_link_ids())
        for link_id, link in dataset.trace_df.itertuples():
            self._add_2_layer(link[TraceKeys.SOURCE], self.source_layers)
            self._add_2_layer(link[TraceKeys.TARGET], self.target_layers)
        definition = ApiDefinition(source_layers=list(self.source_layers.values()), target_layers=list(self.target_layers.values()),
                                   true_links=self.true_links)
        if self.export_path:
            JsonUtil.save_to_json_file(definition.as_dict(), self.export_path)

        return definition

    def _add_2_layer(self, artifact_id: Union[str, int], artifact_layer: Dict[str, Dict[str, str]]) -> None:
        """
        Adds the artifact to the source or target layer
        :param artifact_id: The id of the artifact
        :param artifact_layer: The layer to add the artifact to
        :return: None
        """
        artifact = self.get_dataset().artifact_df.get_artifact(artifact_id)
        if artifact[ArtifactKeys.LAYER_ID] not in artifact_layer:
            artifact_layer[artifact[ArtifactKeys.LAYER_ID]] = {}
        if artifact_id not in artifact_layer[artifact[ArtifactKeys.LAYER_ID]]:
            artifact_layer[artifact[ArtifactKeys.LAYER_ID]][artifact_id] = artifact[ArtifactKeys.CONTENT]

    @staticmethod
    def include_filename() -> bool:
        """
        Returns True bc the dataset exporter expects the export path to include the filename
        :return: True
        """
        return True
