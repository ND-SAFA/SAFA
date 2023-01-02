import os
from typing import Callable, Dict, List

from util.file_util import FileUtil

ENV_REPLACEMENT_VARIABLES = ["DATA_PATH", "ROOT_PATH", "OUTPUT_PATH"]


def get_env_replacements():
    replacements = {}
    for replacement_path in ENV_REPLACEMENT_VARIABLES:
        path_value = os.environ.get(replacement_path, None)
        if path_value:
            path_key = "[%s]" % replacement_path
            replacements[path_key] = os.path.expanduser(path_value)
    return replacements


def read_job_definition(file_path: str):
    file_path = os.path.expanduser(file_path)
    env_replacements = get_env_replacements()
    job_definition = FileUtil.read_json_file(file_path)
    return FileUtil.expand_paths_in_dictionary(job_definition, env_replacements)


def get_path(entry_dict: Dict, paths: List[str]):
    if len(paths) == 0:
        return entry_dict
    current_key = paths[0]
    next_keys = paths[1:]
    if current_key not in entry_dict:
        raise ValueError("Could not find %s in %s." % (current_key, entry_dict))
    return get_path(entry_dict[current_key], next_keys)


def filter_entries(entry_dict: Dict, filter: Callable[[str], bool] = lambda s: s):
    return {k: v for k, v in entry_dict.items() if filter(k)}


def ls_filter(path: str, f: Callable[[str], bool] = None, ignore: List[str] = None):
    if f is None:
        f = lambda s: s
    if ignore is None:
        ignore = []
    return list(filter(lambda p: f(p) and p not in ignore, os.listdir(path)))


def ls_jobs(path: str):
    return ls_filter(path, f=lambda p: len(p.split("-")) == 5)


def get_dict_path(data: Dict, instructions: List[str]):
    if len(instructions) == 0:
        return data
    current_key = instructions[0]
    next_keys = instructions[1:]
    return get_dict_path(data[current_key], next_keys)


def extract_info(data: Dict, copy_paths: List[List[str]], ignore=None, log=False):
    if ignore is None:
        ignore = []
    result = {}
    for path in copy_paths:
        try:
            value = get_dict_path(data, path)
            if isinstance(value, dict):
                filter_values = {k: v for k, v in value.items() if k not in ignore}
                result = {**result, **filter_values}
            else:
                result = {**result, path[-1]: value}
        except Exception as e:
            if log:
                print(e)

    return result
