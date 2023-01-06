import json
import os
import shutil
from typing import Dict, List, Union

from util.json_util import JSONUtil


class FileUtil:

    @staticmethod
    def make_dir_safe(output_path: str, *additional_path_parts) -> str:
        """
        Makes a directory, by first checking if the directory exists
        :return: the output path
        """
        if additional_path_parts:
            output_path = os.path.join(output_path, *additional_path_parts)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return output_path

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

    @staticmethod
    def save_to_file(content: Union[str, Dict], output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        if isinstance(content, dict):
            content = JSONUtil.dict_to_json(content)
        with FileUtil.safe_open_w(output_file_path) as file:
            file.write(content)

    @staticmethod
    def safe_open_w(path):
        FileUtil.create_dir(path)
        return open(path, 'w')

    @staticmethod
    def create_dir(dir_path: str):
        if not os.path.exists(os.path.dirname(dir_path)):
            os.makedirs(os.path.dirname(dir_path))

    @staticmethod
    def delete_dir(dir_path: str) -> None:
        """
        Deletes folder and everything inside it.
        :param dir_path: The path to the folder.
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
