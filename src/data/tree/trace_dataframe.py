from collections import OrderedDict
from typing import Any

import pandas as pd
from pandas._typing import Axes, Dtype
from pandas.core.internals.construction import dict_to_mgr

from data.keys.structure_keys import StructuredKeys
from data.tree.trace_link import TraceLink

TraceKeys = StructuredKeys.Trace


class TraceDataFrame(pd.DataFrame):
    """
    Represents the config format for all data used by the huggingface trainer.
    """
    COLUMNS = {val for name, val in vars(TraceKeys).items() if not name.startswith("__")}

    def __init__(self, data=None, index: Axes = None, columns: Axes = None, dtype: Dtype = None, copy: bool = None):
        """
        Extends
        """
        super().__init__(data, index, columns, dtype, copy)
        self.assert_columns()
        self.add_link_ids()

    def add_link_ids(self) -> None:
        """
        Adds the link ids column to the df
        :return: None
        """
        if self.columns.empty:
            return
        if TraceKeys.LINK_ID not in self.columns:
            link_ids = []
            for index, row in self.iterrows():
                link_ids.append(TraceLink.generate_link_id(row[TraceKeys.SOURCE], row[TraceKeys.TARGET]))
            self[TraceKeys.LINK_ID] = link_ids
        self.set_index(TraceKeys.LINK_ID, inplace=True)

    def add_link(self, source_id: str = None, target_id: str = None, label: int = 0) -> pd.DataFrame:
        """
        Adds link to dataframe
        :param source_id: The id of the source, only required if link_id is not specified
        :param target_id: The id of the target, only required if link_id is not specified
        :param label: The label of the link (1 if True link, 0 otherwise)
        :return: The newly added link
        """
        link_id = TraceLink.generate_link_id(source_id, target_id)
        if link_id not in self.index:
            link = OrderedDict({TraceKeys.SOURCE: source_id, TraceKeys.TARGET: target_id, TraceKeys.LABEL: label})
            if self.columns.empty:
                mgr = dict_to_mgr({key: [val] for key, val in link.items()}, None, None)
                object.__setattr__(self, "_mgr", mgr)
                self.add_link_ids()
            else:
                self.loc[link_id] = list(link.values())
        return self.loc[[link_id]]

    def get_link(self, link_id: int = None, source_id: str = None, target_id: str = None) -> pd.DataFrame:
        """
        Gets the row of the dataframe with the associated link_id or source and target id
        :param link_id: The id of the link to get. May provide source and target id instead
        :param source_id: The id of the source, only required if link_id is not specified
        :param target_id: The id of the target, only required if link_id is not specified
        :return: The link if one is found with the specified params, else None
        """
        if link_id is None:
            assert source_id and target_id, "Requires source_id and target_id if no link_id is provided."
            link_id = TraceLink.generate_link_id(source_id, target_id)
        try:
            link = self.loc[[link_id]]
        except KeyError as e:
            link = None
        return link

    def assert_columns(self) -> None:
        """
        Asserts that all columns are those expected in the DF
        :return: None
        """
        if self.columns.empty:
            return
        columns = {col.lower() for col in self.columns}
        missing_columns = self.COLUMNS.difference(columns)
        if TraceKeys.LINK_ID in missing_columns:
            missing_columns.remove(TraceKeys.LINK_ID)
        assert len(missing_columns) == 0, f"Expected the following columns to be present in the trace df: {missing_columns}. " \
                                          f"Received instead {self.columns}"
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
