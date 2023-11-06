import ast
import json
import os
import sys
from _ast import AST
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv()
ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
sys.path.append(ROOT_PATH)

from tgen.common.util.file_util import FileUtil

NodeType = AST
EXCLUDES = ["tgen/tgen/testres", "tgen/test"]
INCLUDES = [os.path.join(ROOT_PATH, "tgen")]


def print_missing_headers(directory_paths: List[str] = INCLUDES, throw_error: bool = False) -> None:
    """
    Finds all functions and methods not containing a doc-string.
    :param directory_paths: The paths to check for python files.
    :param throw_error: Whether to throw error if invalid functions/methods found.
    :return: None
    """
    missing_map = {}
    for directory_path in directory_paths:
        path_map = calculate_missing_doc_map(directory_path)
        path_map = {k: v for k, v in path_map.items() if len(v) > 0}
        path_map = {get_display_name(k, directory_path): v for k, v in path_map.items()}
        missing_map.update(path_map)

    if len(missing_map) > 0:
        missing_header_message = json.dumps(missing_map, indent=4)
        if throw_error:
            raise Exception(f"{missing_header_message}\nMissing docs.")
        else:
            print(missing_header_message)
    else:
        print("No missing docs :)")


def filter_files(file_path: str):
    """
    Returns whether given file should be included in analysis.
    :param file_path: Path to file.
    :return: True if valid for analyzing.
    """
    file_name = os.path.basename(file_path)
    is_exclude = any([p in file_path for p in EXCLUDES])
    return os.path.isfile(file_path) and file_name.endswith(".py") and file_name != "__init__.py" and not is_exclude


def calculate_missing_doc_map(directory_path: str) -> Dict[str, List[str]]:
    """
    Creates a map from files to their descriptions of their missing doc functions.
    :param directory_path: The directory to traverse.
    :return: Map of file paths to their errors.
    """
    missing_map = {}
    files = [f for f in FileUtil.get_all_paths(directory_path) if filter_files(f)]
    for file_path in files:
        file_content = FileUtil.read_file(file_path)
        tree = ast.parse(file_content, filename=file_path)

        if file_path not in missing_map:
            missing_map[file_path] = []

        for node in ast.walk(tree):
            if has_docstring(node) and ast.get_docstring(node) is None:
                msg = f"Missing docstring in {type(node).__name__} '{node.name}' at line {node.lineno}."
                missing_map[file_path].append(msg)

    return missing_map


def has_docstring(node):
    """
    Checks to see if node contains a docstring to check.
    :param node:
    :return:
    """
    return isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) \
        or isinstance(node, ast.ClassDef) and (ast.get_docstring(node) is not None)


def get_display_name(file_path: str, root_path: str):
    """
    Gets the name to display for file path.
    :param file_path: The path to a python file.
    :param root_path: THe path to the root of project.
    :return: Relative file path to file with the directory name included.
    """
    directory_name = os.path.basename(root_path)
    relative_path = os.path.relpath(file_path, root_path)
    display_path = os.path.join(directory_name, relative_path)
    return display_path


if __name__ == "__main__":
    print_missing_headers(INCLUDES, throw_error=True)
