import json
from typing import Dict


class FileUtil:
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
