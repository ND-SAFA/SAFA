import ast
import os
import sys
from _ast import AST, ClassDef, FunctionDef, arg
from typing import Callable, List, Union

from dotenv import load_dotenv
from mccabe import get_module_complexity

load_dotenv()
ROOT_PATH = os.path.expanduser(os.environ["ROOT_PATH"])
sys.path.append(ROOT_PATH)

NodeType = AST
EXCLUDES = ["tgen/tgen/testres", "tgen/test", "venv"]
DEFAULT_TGEN_PATH = os.path.join(ROOT_PATH, "tgen")
IGNORED_PARAM_NAMES = ["self", "cls", "_"]
DEFAULT_COMPLEXITY_THRESHOLD = 7


def read_file(f_path: str):
    with open(f_path) as f:
        return f.read()


def get_all_paths(dir_path: Union[List[str], str], condition: Callable = None) -> List[str]:
    """
    Reads all code files in directory with allowed extensions.
    :param dir_path: Path to directory where code files live
    :param condition: A callable that returns True if the filepath should be included
    :return: List containing all code file paths.
    """
    if isinstance(dir_path, list):
        paths = set()
        for p in dir_path:
            paths.update(set(get_all_paths(p)))
        return list(paths)
    condition = condition if condition is not None else lambda x: True
    file_paths = []
    for subdir, dirs, files in os.walk(dir_path):
        for f in files:
            if condition(f):
                file_paths.append(os.path.join(subdir, f))
    return file_paths


class DocNode:
    def __init__(self, node, file_path: str):
        """
        Creates node in a file
        :param node: The node.
        :param file_path: Path to parent file.
        """
        self.node = node
        self.file_path = file_path

    def get_name(self) -> str:
        """
        :return: Name of node (e.g. function / class name)
        """
        return self.node.name

    def get_type_name(self) -> str:
        """
        :return: The name of the type of node.
        """
        return type(self.node).__name__

    def get_line_no(self):
        """
        :return: Line number starting node definition.
        """
        return self.node.lineno

    def get_docstring(self):
        """
        :return: The docstring of node.
        """
        return ast.get_docstring(self.node)

    def has_docstring(self):
        """
        :return: Whether this node contains a doc string.
        """
        return has_docstring(self.node)

    def is_function(self) -> bool:
        """
        :return: Whether node is function definition.
        """
        return isinstance(self.node, FunctionDef)

    def is_class(self) -> bool:
        """
        :return: Whether node is class definition.
        """
        return isinstance(self.node, ClassDef)

    def get_errors(self) -> List[str]:
        """
        Gets errors occurring in node within a file.
        :return: List of errors.
        """
        errors = []
        doc_string = self.get_docstring()
        if doc_string is None:
            link = get_link(self.file_path, self.get_line_no())
            errors.append(f"{link}: Missing docstring in '{self.get_name()}'.")

        if doc_string and self.is_function():
            for node_arg in self.node.args.args:
                arg_name = node_arg.arg
                if arg_name in IGNORED_PARAM_NAMES:
                    continue
                if in_docstring(node_arg, doc_string):
                    continue
                link = get_link(self.file_path, node_arg.lineno)
                msg = f"{link}: Missing param `{node_arg.arg}` in '{self.get_name()}'."
                errors.append(msg)
        return errors


class FileNode:
    def __init__(self, file_path: str):
        """
        Creates node representing python file.
        :param file_path: Path to file.
        """
        self.file_path = file_path
        self.nodes = self.get_file_nodes(self.file_path)

    @staticmethod
    def get_file_nodes(file_path: str) -> List[DocNode]:
        """
        Reads nodes in file.
        :param file_path: The path to file to read nodes from.
        :return: List of nodes.
        """
        file_content = read_file(file_path)
        tree = ast.parse(file_content, filename=file_path)
        nodes = [DocNode(node, file_path) for node in ast.walk(tree)]
        return nodes

    def get_errors(self) -> List[str]:
        """
        Returns errors found in nodes of file.
        :return: List of errors.
        """
        errors = []
        for node in self.nodes:
            if not node.has_docstring():
                continue

            errors.extend(node.get_errors())
        return errors


def print_missing_headers(paths: List[str] = None, throw_error: bool = False) -> None:
    """
    Finds all functions and methods not containing a doc-string.
    :param paths: List of paths to check for missing docs.
    :param throw_error: Whether to throw error if invalid functions/methods found.
    :return: None
    """
    if paths is None or len(paths) == 0:
        paths = [DEFAULT_TGEN_PATH]

    for directory_path in paths:
        errors = calculate_missing_doc_map(directory_path)

    if len(errors) > 0:
        print_errors(errors)
        if throw_error:
            raise Exception("Missing docs.")
    else:
        print("No missing docs :)")


def print_errors(errors: List[str]):
    """
    Prints list of errors.
    :param errors: The errors to print.
    :return: None
    """
    for e in errors:
        print(e)
    print(f"{len(errors)} errors found.")


def filter_files(file_path: str):
    """
    Returns whether given file should be included in analysis.
    :param file_path: Path to file.
    :return: True if valid for analyzing.
    """
    file_name = os.path.basename(file_path)
    is_exclude = any([p in file_path for p in EXCLUDES])
    return os.path.isfile(file_path) and file_name.endswith(".py") and file_name != "__init__.py" and not is_exclude


def calculate_missing_doc_map(directory_path: str) -> List[str]:
    """
    Creates a map from files to their descriptions of their missing doc functions.
    :param directory_path: The directory to traverse.
    :return: Map of file paths to their errors.
    """
    files = [f for f in get_all_paths(directory_path) if filter_files(f)]
    print(f"Checking {len(files)} files in {directory_path}...")
    errors = []
    for file_path in files:
        file_node = FileNode(file_path)
        file_errors = file_node.get_errors()
        errors.extend(file_errors)
    return errors


def in_docstring(arg: arg, docstring: str):
    """
    Checks if arg contains doc in function docstring.
    :param arg: Argument to function.
    :param docstring: Docstring of function.
    :return: True if arg contains doc.
    """
    arg_name = arg.arg
    if arg_name in IGNORED_PARAM_NAMES:
        return True
    for line in docstring.splitlines():
        query = f":param {arg_name}"
        if query in line:
            arg_doc = line[line.index(query):].strip()
            return len(arg_doc) > 0
    return False


def has_docstring(node):
    """
    Checks to see if node contains a docstring to check.
    :param node:
    :return:
    """
    return isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef) \
        or isinstance(node, ast.ClassDef) and (ast.get_docstring(node) is not None)


def get_link(file_path: str, line_number):
    """
    Gets the name to display for file path.
    :param file_path: The path to a python file.
    :param line_number: The line the error occurred at.
    :return: pycharm printable url.
    """
    display_path = f"File \"{file_path}\", line {line_number}"
    return display_path


def print_complex_functions(paths: List[str] = None, threshold: int = DEFAULT_COMPLEXITY_THRESHOLD):
    """
    Prints the complexity of functions exceed complexity threshold.
    :param paths: List of paths to check for complex functions.
    :param threshold: The threshold of the complexity to filter by.
    :return: None.
    """
    if paths is None or len(paths) == 0:
        paths = [DEFAULT_TGEN_PATH]
    files = [f for directory_path in paths for f in get_all_paths(directory_path) if filter_files(f)]
    for file in files:
        get_module_complexity(file, threshold=threshold)


if __name__ == "__main__":
    direction_paths = sys.argv[1:]
    print_missing_headers(direction_paths)
