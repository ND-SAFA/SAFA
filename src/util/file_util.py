import json
import os
from typing import Dict, List, Union


class FileUtil:

    @staticmethod
    def make_dir_safe(output_path: str) -> None:
        """
        Makes a directory, by first checking if the directory exists
        :return: None
        """
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    @staticmethod
    def read_file(file_path: str):
        """
        Reads file at given path if exists.
        :param file_path: Path of the file to read.
        :return: The content of the file.
        """
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def read_json_file(file_path: str) -> Dict:
        """
        Reads JSON from file at path.
        :param file_path: Path to JSON file.
        :return: Dictionary content of file.
        """
        with open(file_path) as file:
            return json.load(file)

    @staticmethod
    def get_file_list(data_path: str, exclude: List[str] = None) -> List[str]:
        """
        Gets list of files in the data path
        :param data_path: the path to the data
        :param exclude: list of strings to exclude
        :return: a list of files
        """
        if exclude is None:
            exclude = [".DS_Store"]
        if os.path.isfile(data_path):
            files = [data_path]
        elif os.path.isdir(data_path):
            files = list(filter(lambda f: f not in exclude, os.listdir(data_path)))
            files = list(map(lambda f: os.path.join(data_path, f), files))
        else:
            raise Exception("Unable to read pretraining data file path " + data_path)
        return files

    @staticmethod
    def expand_paths_in_dictionary(value: Union[List, Dict, str], replacements: Dict[str, str] = None):
        """
        For every string found in value, if its a path its expanded and
        :param value: List, Dict, or String containing one or more values.
        :param replacements: Dictionary from source to target string replacements in paths.
        :return: Same type as value, but with its content processed.
        """
        if isinstance(value, list):
            return [FileUtil.expand_paths_in_dictionary(v, replacements=replacements) for v in value]
        if isinstance(value, dict):
            return {k: FileUtil.expand_paths_in_dictionary(v, replacements=replacements) for k, v in value.items()}
        if isinstance(value, str):
            if "~" in value:
                return os.path.expanduser(value)
            if replacements:
                for k, v in replacements.items():
                    value = value.replace(k, v)
        return value
