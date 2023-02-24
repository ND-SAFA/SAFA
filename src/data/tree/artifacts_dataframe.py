from collections import OrderedDict
from typing import Any

import pandas as pd
from pandas._typing import Axes, Dtype
from pandas.core.internals.construction import dict_to_mgr

from data.keys.structure_keys import StructuredKeys

ArtifactKeys = StructuredKeys.Artifact


class ArtifactsDataFrame(pd.DataFrame):
    """
    Represents the config format for all data used by the huggingface trainer.
    """
    COLUMNS = {val for name, val in vars(ArtifactKeys).items() if not name.startswith("__")}

    def __init__(self, data=None, index: Axes = None, columns: Axes = None, dtype: Dtype = None, copy: bool = None):
        """
        Extends
        """
        super().__init__(data, index, columns, dtype, copy)
        self.assert_columns()
        self.set_index(ArtifactKeys.ID, inplace=True)

    def add_artifact(self, artifact_id: Any, body: str, layer_id: Any = 1) -> pd.DataFrame:
        """
        Adds link to dataframe
        :param artifact_id: The id of the Artifact
        :param body: The body of the artifact
        :param layer_id: The id of the layer that the artifact is part of
        :return: The newly added artifact
        """
        if artifact_id not in self.index:
            artifact = OrderedDict({ArtifactKeys.ID: artifact_id, ArtifactKeys.BODY: body, ArtifactKeys.LAYER_ID: layer_id})
            if self.columns.empty:
                mgr = dict_to_mgr({key: [val] for key, val in artifact.items()}, None, None)
                object.__setattr__(self, "_mgr", mgr)
                self.set_index(ArtifactKeys.ID, inplace=True)
            else:
                self.loc[artifact_id] = list(artifact.values())
        return self.loc[[artifact_id]]

    def get_artifact(self, artifact_id: Any) -> pd.DataFrame:
        """
        Gets the row of the dataframe with the associated artifact_id
        :param artifact_id: The id of the artifact to get
        :return: The artifact if one is found with the specified params, else None
        """
        try:
            artifact = self.loc[[artifact_id]]
        except KeyError as e:
            artifact = None
        return artifact

    def assert_columns(self) -> None:
        """
        Asserts that all columns are those expected in the DF
        :return: None
        """
        if self.columns.empty:
            return
        columns = {col.lower() for col in self.columns}
        missing_columns = self.COLUMNS.difference(columns)
        assert len(missing_columns) == 0, f"Expected the following columns to be present in the trace df: {missing_columns}"
        unexpected_columns = columns.difference(self.COLUMNS)
        assert len(unexpected_columns) == 0, f"Unexpected columns in the trace df: {unexpected_columns}"

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Sets an item for the dataframe
        :param key: The key to set
        :param value: The value to set
        :return: None
        """
        super().__setitem__(key, value)
        self.assert_columns()
        self.set_index(ArtifactKeys.ID, inplace=True)
