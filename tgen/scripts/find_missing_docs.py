import ast
import json
import os
from _ast import AST

from dotenv import load_dotenv

load_dotenv()

EXCLUDES = ["tgen/tgen/testres", "tgen/test"]

NodeType = AST


def has_docstring_2(node: NodeType):
    """
    Check if the given AST node has a docstring.
    :param node:
    :return:
    """
    allowable_node_types = [ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
    is_allowable = any([isinstance(node, node_type) for node_type in allowable_node_types])
    return is_allowable and (ast.get_docstring(node) is not None)


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


def find_functions_classes_methods_without_docstring(directory_path: str):
    """Find functions, classes, and methods without a docstring in the given directory."""
    missing_map = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py") and not file == "__init__.py":
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                    except SyntaxError as e:
                        print(f"Error parsing {file_path}: {e}")
                        continue

                    is_exclude = any([p in file_path for p in EXCLUDES])
                    if is_exclude:
                        continue

                    if file_path not in missing_map:
                        missing_map[file_path] = []

                    for node in ast.walk(tree):
                        if has_docstring(node) and ast.get_docstring(node) is None:
                            msg = f"Missing docstring in {type(node).__name__} '{node.name}' at line {node.lineno}."
                            missing_map[file_path].append(msg)
    missing_map = {k: v for k, v in missing_map.items() if len(v) > 0}
    if len(missing_map) > 0:

        missing_map = {get_display_name(k, directory_path): v for k, v in missing_map.items()}
        raise Exception(f"{json.dumps(missing_map, indent=4)}\nMissing docs.")
    else:
        print("No missing docs :)")


def main():
    """
    TODO
    :return:
    """
    directory_path = os.path.expanduser(os.environ["ROOT_PATH"])
    find_functions_classes_methods_without_docstring(directory_path)


if __name__ == "__main__":
    main()
