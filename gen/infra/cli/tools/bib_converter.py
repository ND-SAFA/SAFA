"""
The following file is intended to help construct latex tables from CSVs.
"""
import os
import sys
from typing import Dict, List

import pandas as pd
from gen_common.constants.env_var_name_constants import OUTPUT_PATH_PARAM, ROOT_PATH_PARAM
from gen_common.constants.symbol_constants import PERIOD
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = os.path.expanduser(os.environ[ROOT_PATH_PARAM])
assert os.path.exists(ROOT_PATH), ROOT_PATH
sys.path.append(ROOT_PATH)

OUTPUT_PATH = os.path.expanduser(os.environ[OUTPUT_PATH_PARAM])
RESULTS_PATH = os.path.join(OUTPUT_PATH, "results")


def write_row(entries: List[Dict]):
    """
    Writes the latex for a row given list of instructions per entry.
    :param entries: Per entry instructions containing value and other settings.
    :return: String representing latex text for row.
    """
    row = ""

    for i, entry in enumerate(entries):
        prefix = " & " if row != "" else ""
        suffix = " \\\\ \\hline \n" if i == len(entries) - 1 else ""
        value = entry["value"]
        if "bold" in entry and entry["bold"]:
            value = "\\textbf{%s}" % value
        if isinstance(value, int) or isinstance(value, float):
            value = str(round(value, 2))
        row += prefix + value + suffix

    return row


def write_columns(df: pd.DataFrame):
    """
    Writes the columns of dataframe as a latex row in a table.
    :param df: The dataframe whose columns are written.
    :return: String representing latex row.
    """
    column_definitions = [{"value": c, "bold": True} for c in df.columns]
    return write_row(column_definitions)


def read_aggregate_df(folder_path: str, column_sort: List[str]):
    """
    Reads files and aggregates them into single dataset, sorting at the end.
    :param folder_path: The path to the folder to aggregate.
    :param column_sort: The sorting order of the columns.
    :return: DataFrame
    """
    result_files = list(filter(lambda f: f[0] != PERIOD, os.listdir(folder_path)))
    result_files = list(map(lambda f: os.path.join(folder_path, f), result_files))
    df = None
    for data_path in result_files:
        current_df = pd.read_csv(data_path)
        df = pd.concat([current_df, df], ignore_index=True)
    df = df.sort_values(column_sort, ascending=False)
    return df[column_sort]


if __name__ == "__main__":
    latex = "\\hline"
    sort = ["Project", "Model", "MAP", "AP", "F1", "F2"]
    df = read_aggregate_df(RESULTS_PATH, sort)
    latex += write_columns(df)
    for i, entry in df.iterrows():
        entry_definitions = []
        for column in df.columns:
            entry_definitions.append({
                "value": entry[column]
            })
        latex += write_row(entry_definitions)

    print(latex)
