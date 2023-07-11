from typing import Any, Dict, Type

from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.util.enum_util import EnumDict

TraceKeys = StructuredKeys.Trace


class TraceDataFrame(AbstractProjectDataFrame):
    """
    Contains the trace links found in a project
    """
    OPTIONAL_COLUMNS = [StructuredKeys.Trace.SCORE.value]

    def __init__(self, *args, **kwargs):
        """
        Creates constructor with guaranteed columns for trace dataframe.
        :param args: The positional arguments to constructor trace dataframe with.
        :param kwargs: The keyword arguments to construct trace dataframe with.
        """
        if "columns" not in kwargs:
            kwargs["columns"] = StructuredKeys.Trace.get_cols()
        super().__init__(*args, **kwargs)

    @classmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """
        return TraceKeys.LINK_ID.value

    @classmethod
    def data_keys(cls) -> Type:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """
        return TraceKeys

    def process_data(self) -> None:
        """
        Sets the index of the dataframe and performs any other processing steps
        :return: None
        """
        self.add_link_ids()
        super().process_data()

    def add_link_ids(self) -> None:
        """
        Adds the link ids column to the df
        :return: None
        """
        if self.columns.empty:
            return
        if TraceKeys.LINK_ID.value not in self.columns and self.index.name != self.index_name():
            link_ids = []
            for index, row in self.itertuples():
                link_ids.append(TraceDataFrame.generate_link_id(row[TraceKeys.SOURCE], row[TraceKeys.TARGET]))
            self[TraceKeys.LINK_ID] = link_ids

    def add_link(self, source_id: str, target_id: str, label: int = 0) -> EnumDict:
        """
        Adds link to dataframe
        :param source_id: The id of the source
        :param target_id: The id of the target
        :param label: The label of the link (1 if True link, 0 otherwise)
        :return: The newly added link
        """
        link_id = TraceDataFrame.generate_link_id(source_id, target_id)
        return self.add_new_row(self.link_as_dict(source_id, target_id, label, link_id))

    def get_link(self, link_id: int = None, source_id: str = None, target_id: str = None) -> EnumDict:
        """
        Gets the row of the dataframe with the associated link_id or source and target id
        :param link_id: The id of the link to get. May provide source and target id instead
        :param source_id: The id of the source, only required if link_id is not specified
        :param target_id: The id of the target, only required if link_id is not specified
        :return: The link if one is found with the specified params, else None
        """
        if link_id is None:
            assert source_id is not None and target_id is not None, "Requires source_id and target_id if no link_id is provided."
            link_id = TraceDataFrame.generate_link_id(source_id, target_id)
        return self.get_row(link_id)

    @staticmethod
    def link_as_dict(source_id: str, target_id: str, label: int = 0, link_id: int = None) -> Dict[TraceKeys, Any]:
        """
        Creates a dictionary mapping column names to the corresponding link information
        :param source_id: The id of the source artifact
        :param target_id: The id of the target artifact
        :param label: The label of the link (1 if True link, 0 otherwise)
        :param link_id: The id of the link
        :return: A dictionary mapping column names to the corresponding link information
        """
        dict_ = EnumDict({TraceKeys.LINK_ID: link_id} if link_id else {})
        dict_.update({TraceKeys.SOURCE: source_id, TraceKeys.TARGET: target_id, TraceKeys.LABEL: label})
        return dict_

    @staticmethod
    def generate_link_id(source_id: Any, target_id: Any) -> int:
        """
        Generates a unique id for a source, target link
        :param source_id: id of source artifact
        :param target_id: id of target artifact
        :return: the link id
        """
        return hash(str(hash(source_id)) + "-" + str(hash(target_id)))

    def get_label_count(self, label: int = 1) -> int:
        """
        :return: Returns the number of true positives in data frame.
        """
        label_counts = self[TraceKeys.LABEL].value_counts()
        n_label = label_counts.get(label, 0)
        return n_label
