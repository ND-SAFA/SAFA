from typing import Dict, List

import pandas as pd

from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from gen_common.data.keys.structure_keys import ArtifactKeys, LayerKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.objects.trace import Trace
from gen_common.data.objects.trace_layer import TraceLayer
from gen_common.data.readers.definitions.api_definition import ApiDefinition
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.util.json_util import JsonUtil


class ApiExporter(AbstractDatasetExporter):

    def __init__(self, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None, export_path: str = EMPTY_STRING):
        """
        Initializes exporter for given trace dataset.
        :param dataset: The dataset to export
        :param dataset_creator: The creator in charge of making the dataset to export
        :param export_path: The path to export the dataset to
        """
        super().__init__(dataset_creator=dataset_creator, dataset=dataset, export_path=export_path)
        self.artifacts: List[Artifact] = []
        self.true_links: List[Trace] = []

    def export(self, **kwargs) -> ApiDefinition:
        """
        Exports the dataset to the ApiDefinition format
        :return: The ApiDefinition
        """
        dataset = self.get_dataset()
        trace_df: TraceDataFrame = dataset.trace_df
        self.true_links: List[Dict] = trace_df.get_links(true_only=True)
        artifacts: List[Artifact] = dataset.artifact_df.to_dict("records", index=True)

        layers = []
        for i, layer_row in dataset.layer_df.itertuples():
            parent_type = layer_row[LayerKeys.TARGET_TYPE]
            child_type = layer_row[LayerKeys.SOURCE_TYPE]
            layers.append(TraceLayer(parent=parent_type, child=child_type))

        definition = ApiDefinition(layers=layers,
                                   artifacts=artifacts,
                                   links=self.true_links)
        if self.export_path:
            JsonUtil.save_to_json_file(definition, self.export_path)

        return definition

    def _add_artifact(self, artifact: pd.Series) -> None:
        """
        Adds the artifact to the source or target layer
        :param artifact: The id of the artifact
        :return: None
        """
        artifact_id = artifact[ArtifactKeys.ID.value]
        layer_id = artifact[ArtifactKeys.LAYER_ID.value]
        content = artifact[ArtifactKeys.CONTENT.value]

        if layer_id not in self.generated_layers:
            self.generated_layers[layer_id] = {}

        if artifact_id not in self.generated_layers[layer_id]:
            self.generated_layers[layer_id][artifact_id] = content

    @staticmethod
    def include_filename() -> bool:
        """
        Returns True bc the dataset exporter expects the export path to include the filename
        :return: True
        """
        return True
