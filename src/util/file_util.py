import json
import os
from typing import Dict, List


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
