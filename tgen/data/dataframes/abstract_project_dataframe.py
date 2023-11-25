from abc import abstractmethod
from copy import deepcopy
from enum import Enum
from typing import Any, Callable, Dict, List, Type, Union

import pandas as pd
from pandas._typing import Axes, Dtype
from pandas.core.internals.construction import dict_to_mgr

from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict, EnumUtil
from tgen.common.logging.logger_manager import logger
from tgen.common.util.override import overrides


class AbstractProjectDataFrame(pd.DataFrame):
    """
    Represents the config format for all data used by the huggingface trainer.
    """
    __COLS = None
    OPTIONAL_COLUMNS: List[str] = []

    def __init__(self, data=None, index: Axes = None, columns: Axes = None, dtype: Dtype = None, copy: bool = None):
        """
        Extends the pandas dataframe for all trace project information
        :param data: The data used to initialize data frame.
        :param index: The index of the datums.
        :param columns: The columns of the data frame.
        :param dtype: The type of data contained in each column.
        :param copy: Whether to create a copy of the data frame.
        """
        if isinstance(data, pd.DataFrame) and not isinstance(data, self.__class__):
            data = data[[col.value for col in self.data_keys() if col.value in data.columns]]
        if isinstance(data, dict) and not isinstance(data, EnumDict):
            data = EnumDict(data)
        if columns is not None and isinstance(columns[0], Enum):
            columns = [col.value for col in columns]
        super().__init__(data, index, columns, dtype, copy)
        self.assert_columns()
        self.process_data()

    @classmethod
    def required_column_names(cls) -> List[str]:
        """
        Returns the names of the columns in the dataframe
        :return: A set containing the names of the columns in the dataframe
        """
        if cls.__COLS is None:
            cls.__COLS = [e.value for e in cls.data_keys() if e not in cls.OPTIONAL_COLUMNS]
        return cls.__COLS

    def get_all_column_names(self) -> List[str]:
        """
        Gets the name of all columns
        :return: The name of all columns
        """
        return [e.value for e in self.data_keys() if e.value != self.index_name()]

    @classmethod
    @abstractmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """

    @classmethod
    @abstractmethod
    def data_keys(cls) -> Enum:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """

    def process_data(self) -> None:
        """
        Sets the index of the dataframe and performs any other processing steps
        :return: None
        """
        if self.index_name() is not None and not self.columns.empty and self.index.name != self.index_name():
            self.set_index(self.index_name(), inplace=True)

    def add_or_update_row(self, row_as_dict: Dict[Union[Enum, str], Any]) -> EnumDict:
        """
        Adds row to dataframe
        :param row_as_dict: Dictionary mapping column name to its value
        :return: The newly added row as a tuple
        """
        row_as_dict = EnumDict(row_as_dict)
        index = row_as_dict.get(self.index_name(), len(self.index))
        if index not in self:
            self.assert_columns([col for col in row_as_dict.keys()])
            if self.columns.empty:
                mgr = dict_to_mgr({key: [val] for key, val in row_as_dict.items()}, None, None)
                object.__setattr__(self, "_mgr", mgr)
                self.process_data()
            else:
                if self.index_name() in row_as_dict:
                    row_as_dict.pop(self.index_name())
                self.loc[index] = [row_as_dict.get(col, None) for col in self.get_all_column_names() if col in self.columns]
        return self.get_row(index)

    def get_row(self, index: Any) -> EnumDict:
        """
        Gets the row of the dataframe with the given index
        :param index: The index of the row to get
        :return: The row as a dictionary if index is found else None
        """
        try:
            row_df = self.loc[[index]]
            row_as_dict = EnumDict({col: row_df[col].values[0] for col in self.get_all_column_names() if col in self.columns})
            if self.index_name():
                row_as_dict[self.index_name()] = index
        except KeyError as e:  # index not in dataframe
            row_as_dict = None
        return row_as_dict

    def assert_columns(self, columns: List[str] = None) -> None:
        """
        Asserts that all columns are those expected in the DF
        :param columns: The expected columns in data frame.
        :return: None
        """
        if self.columns.empty and columns is None:
            return
        columns = self.columns if columns is None else columns
        columns = [col.value if isinstance(col, Enum) else col.lower() for col in columns if col is not None]
        expected_columns = deepcopy(self.required_column_names())
        expected_columns = [c for c in expected_columns if c not in self.OPTIONAL_COLUMNS]
        if self.index_name() and self.index_name() not in columns:
            expected_columns.remove(self.index_name())
        missing_columns = set(expected_columns).difference(columns)
        assert len(missing_columns) == 0, f"Expected the following columns to be present in the df: {missing_columns}. " \
                                          f"Received instead {columns}"
        unexpected_columns = set(columns).difference(expected_columns)
        unexpected_columns = [c for c in unexpected_columns if c not in self.OPTIONAL_COLUMNS]

        assert len(unexpected_columns) == 0, f"Unexpected columns in the data frame: {unexpected_columns}"
        i = 0
        for col in expected_columns:
            if col == self.index_name() and columns[i] != col:
                continue
            assert col == columns[
                i], f"Columns expected to be in the following order: {expected_columns} but received {columns[i]} instead of {col}"
            i += 1

    @classmethod
    def concat(cls, dataframe1: "AbstractProjectDataFrame", dataframe2: "AbstractProjectDataFrame",
               ignore_index: bool = False) -> "AbstractProjectDataFrame":
        """
        Combines two dataframes
        :param dataframe1: The first dataframe
        :param dataframe2: The second dataframe
        :param ignore_index: If True, do not use the index values along the concatenation axis.
        :return: The new combined dataframe
        """
        orient = 'records' if ignore_index else 'index'
        data1 = dataframe1.remove_duplicate_indices().to_dict(orient=orient)
        data2 = dataframe2.remove_duplicate_indices().to_dict(orient=orient)
        if ignore_index:
            data1.extend(data2)
            result = cls(data1)
        else:
            data1.update(data2)
            for index, cols in data1.items():
                cols[cls.index_name()] = index
            result = cls.from_dict(data1.values())
        return result

    @overrides(pd.DataFrame)
    def itertuples(self, index: bool = True, name: str = "Pandas") -> EnumDict:
        """
        Iterate over DataFrame rows as namedtuples.
        :param index: if True, return the index as the first element of the tuple.
        :param name : The name of the returned namedtuples or None to return regular tuples.
        :return enum dictionary of data
        """
        for row in super().itertuples(index, name):
            if hasattr(row, "_asdict"):
                dict_ = EnumDict(row._asdict())
                index = dict_.pop("Index")
                if self.index_name():
                    dict_[self.index_name()] = index
                yield index, dict_  # return index and row to match iterrow api
            else:
                yield row

    def filter_by_row(self, filter_lambda: Callable) -> "AbstractProjectDataFrame":
        """
        Returns a copy of the dataframe with filter applied to rows
        :param filter_lambda: The lambda used to filter out rows
        :return: A copy of the dataframe with filter applied to rows
        """
        return self.__class__(DataFrameUtil.filter_df_by_row(self, filter_lambda))

    def filter_by_index(self, index_to_filter: List) -> "AbstractProjectDataFrame":
        """
        Returns a copy of the dataframe with filter applied to rows
        :param index_to_filter: The list of indices to keep.
        :return: A copy of the dataframe with filter applied to rows
        """
        return self.__class__(DataFrameUtil.filter_df_by_index(self, index_to_filter))

    def remove_rows(self, row_ids: List[str]) -> None:
        """
        Removes rows with given ids.
        :param row_ids: The ids of the rows to remove.
        :return: None
        """
        for r_id in row_ids:
            self.remove_row(r_id)

    def remove_row(self, row_id: str) -> None:
        """
        Removes row with given id.
        :param row_id: The id of the row to remove.
        :return: None
        """
        self.drop(row_id, inplace=True)

    def remove_duplicate_indices(self) -> "AbstractProjectDataFrame":
        """
        Removes duplicated indices
        :return: The DataFrame without duplicated indices
        """
        is_duplicated = self.index.duplicated(keep='first')
        duplicated_indices = set(self.index[is_duplicated])
        if len(duplicated_indices) > 0:
            logger.warning(f"Removing {len(duplicated_indices)} duplicates from {self.__class__.__name__}.")
        return self[~is_duplicated]

    @overrides(pd.DataFrame)
    def to_dict(self, orient: str = 'dict', into: Type = dict, index: bool = True) -> Dict:
        """
        Converts the dataframe to dictionary after removing any duplicate indices (panda's to_dict does not allow duplicates)
        :param orient: Determines the type of the values of the dictionary.
        :param into: The collections.abc.Mapping subclass used for all Mappings in the return value.
        :param index: Whether to include the index item
        :return: The dataframe as a dictionary
        """
        if self.index.duplicated(keep='first').any():
            return self.remove_duplicate_indices().to_dict(orient, into, index)
        dict_ = super().to_dict(orient, into, index)
        if index:
            index_name = self.index_name() if self.index_name() else "index"
            if orient == "list":
                dict_[index_name] = self.index
            elif orient == "records":
                for i, d in zip(self.index, dict_):
                    d[index_name] = i
        return dict_

    def update_value(self, column2update: Union[str, Enum], id2update: Union[str, int], new_value: Any) -> None:
        """
        Updates a value in a column
        :param column2update: The name of the column to update
        :param id2update: The id of the row being updated
        :param new_value: The new value to update it to
        :return: None
        """
        if not isinstance(column2update, str):
            column2update = column2update.value
        self.loc[self.index == id2update, column2update] = new_value

    def update_values(self, column2update: Union[str, Enum], ids2update: List[str], new_values: List[Any]) -> None:
        """
         Updates the values of the corresponding ids in a column
         :param column2update: The name of the column to update
         :param ids2update: The list of ids of the rows being updated
         :param new_values: The list of new values to update it to
         :return: None
         """
        for id_, val in zip(ids2update, new_values):
            self.update_value(column2update, id_, val)

    def drop_nan_indices(self) -> pd.DataFrame:
        """
        Drops all columns containing NaN in the index
        :return: A copy of the dataframe without the cols with NaN
        """
        return self.__class__(self[self.index.notnull()])

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Sets an item for the dataframe
        :param key: The key to set
        :param value: The value to set
        :return: None
        """
        super().__setitem__(EnumUtil.to_string(key), value)

    def __getitem__(self, item: Any) -> Any:
        """
        Gets an item for the dataframe
        :param item: The item to get
        :return: The item
        """
        item = EnumUtil.to_string(item)
        return super().__getitem__(item)

    def __contains__(self, item: Any) -> bool:
        """
        Returns True if item in dataframe else False
        :param item: The item to check if it is in the dataframe
        :return: True if item in dataframe else False
        """
        return EnumUtil.to_string(item) in self.index

    def __deepcopy__(self, memodict={}) -> "AbstractProjectDataFrame":
        """
        Deepcopies the dataframe
        :param memodict:
        :return: A deepcopy of the dataframe
        """
        return self.__class__(super().__deepcopy__(self))
