from typing import List, Tuple, Type, Union

from tgen.common.logging.logger_manager import logger
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import LayerKeys


class LayerDataFrame(AbstractProjectDataFrame):
    """
    Contains the layers that are linked found in a project
    """

    @classmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """
        return None

    @classmethod
    def data_keys(cls) -> Type:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """
        return LayerKeys

    @staticmethod
    def from_types(source_types: Union[List[str], str], target_types: Union[List[str], str]):
        """
        Creates layer data frame with single entry.
        :param source_types: The source type of the single entry.
        :param target_types: The target type of the single entry.
        :return: The new layer data frame.
        """
        if isinstance(source_types, str):
            source_types = [source_types]
        if isinstance(target_types, str):
            target_types = [target_types] * len(source_types)

        layer_df = LayerDataFrame()
        for source_type, target_type in zip(source_types, target_types):
            layer_df.add_layer(source_type=source_type, target_type=target_type)
        return layer_df

    def add_layer(self, source_type: str, target_type: str) -> EnumDict:
        """
        Adds linked layers to dataframe
        :param source_type: The type of the source layer
        :param target_type: The type of the target layer
        :return: The newly added linked layer
        """
        return self.add_row({LayerKeys.SOURCE_TYPE: source_type,
                             LayerKeys.TARGET_TYPE: target_type})

    def as_list(self) -> List[Tuple[str, str]]:
        """
        Converts layer data frame into list of strings.
        :return:list of child x parent types.
        """
        tracing_layers = []
        for i, row in self.iterrows():
            child_type = row[LayerKeys.SOURCE_TYPE.value]
            parent_type = row[LayerKeys.TARGET_TYPE.value]
            tracing_layers.append((child_type, parent_type))
        return tracing_layers

    @classmethod
    def concat(cls, *dataframes: "AbstractProjectDataFrame", ignore_index: bool = True) -> "LayerDataFrame":
        """
        Combines two dataframes
        :param dataframes: The data frames to concatenate.
        :param ignore_index: If True, do not use the index values along the concatenation axis.
        :return: The new combined dataframe
        """
        if not ignore_index:
            logger.warning("Index should be ignored for concatenating layer dataframe since they are not unique")
        return super().concat(*dataframes, ignore_index=True)

    def get_layer(self, source_type: str, target_type: str):
        """
        Returns the layer(s) matching the given source and target types.
        :param source_type: The source artifact type.
        :param target_type: The target artifact type.
        :return: Data frame containing query.
        """
        return self.filter_by_row(
            lambda row: row[LayerKeys.SOURCE_TYPE.value] == source_type and row[LayerKeys.TARGET_TYPE.value] == target_type)
