from typing import Type

from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.util.enum_util import EnumDict
from tgen.util.logging.logger_manager import logger

LayerKeys = StructuredKeys.LayerMapping


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

    def add_layer(self, source_type: str, target_type: str) -> EnumDict:
        """
        Adds linked layers to dataframe
        :param source_type: The type of the source layer
        :param target_type: The type of the target layer
        :return: The newly added linked layer
        """
        return self.add_new_row({LayerKeys.SOURCE_TYPE: source_type,
                                 LayerKeys.TARGET_TYPE: target_type})

    @classmethod
    def concat(cls, dataframe1: "AbstractProjectDataFrame", dataframe2: "AbstractProjectDataFrame",
               ignore_index: bool = True) -> "AbstractProjectDataFrame":
        """
        Combines two dataframes
        :param dataframe1: The first dataframe
        :param dataframe2: The second dataframe
        :param ignore_index: If True, do not use the index values along the concatenation axis.
        :return: The new combined dataframe
        """
        if not ignore_index:
            logger.warning("Index should be ignored for concatenating layer dataframe since they are not unique")
        return super().concat(dataframe1, dataframe2, ignore_index=True)
