import os
import shutil
from copy import copy, deepcopy
from dataclasses import dataclass
from inspect import getfullargspec
from os.path import splitext
from typing import Callable, Dict, IO, List, Set, Tuple, Type, Union, get_type_hints

from common_resources.tools.constants.symbol_constants import USER_SYM
from common_resources.tools.util.json_util import JsonUtil


class FileUtilTest:
    class InnerClass:
        TEST = 1

    @staticmethod
    def get_file_ext(path: str) -> str:
        """
        Gets the file extension for a given path
        :param path: The path to get the extension for
        :return: The extension of the file
        """
        return os.path.splitext(path)[-1]

    @staticmethod
    def create_dir_safely(output_path: str, *additional_path_parts) -> str:
        """
        Makes a directory, by first checking if the directory exists
        :return: the output path
        """
        if additional_path_parts:
            output_path = os.path.join(output_path, *additional_path_parts)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    @staticmethod
    def read_file(file_path: str) -> str:
        """
        Reads file at given path if exists.
        :param file_path: Path of the file to read.
        :return: The content of the file.
        """
        with open(file_path, encoding='unicode_escape') as file:
            return file.read()

    @staticmethod
    def get_file_list(data_path: str, exclude: List[str] = None, exclude_ext: List[str] = None) -> List[str]:
        """
        Gets list of files in the data path
        :param data_path: the path to the data
        :param exclude: list of strings to exclude
        :param exclude_ext: list of file extensions to exclude
        :return: a list of files
        """
        if exclude is None:
            exclude = [".DS_Store"]
        if exclude_ext is None:
            exclude_ext = []
        if os.path.isfile(data_path):
            files = [data_path]
        elif os.path.isdir(data_path):
            files = list(filter(lambda f: not (f in exclude or splitext(f)[1] in exclude_ext), os.listdir(data_path)))
            files = list(map(lambda f: os.path.join(data_path, f), files))
            all_files = []
            for file in files:
                all_files.extend(FileUtilTest.get_file_list(file, exclude=exclude, exclude_ext=exclude_ext))
            files = all_files
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
            return [FileUtilTest.expand_paths_in_dictionary(v, replacements=replacements) for v in value]
        if isinstance(value, dict):
            return {k: FileUtilTest.expand_paths_in_dictionary(v, replacements=replacements) for k, v in value.items()}
        if isinstance(value, str):
            if USER_SYM in value:
                return os.path.expanduser(value)
            if replacements:
                for k, v in replacements.items():
                    value = value.replace(k, v)
        return value

    @staticmethod
    def write(content: Union[str, Dict], output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        if isinstance(content, dict):
            content = JsonUtil.dict_to_json(content)
        with FileUtilTest.safe_open_w(output_file_path) as file:
            file.write(content)

    @staticmethod
    def safe_open_w(path: str) -> IO:
        """
        Opens given file without throwing exception if it does not exist
        :param path: the path to file
        :return: the file object
        """
        FileUtilTest.create_dir_safely(os.path.dirname(path))
        return open(path, 'w')

    @staticmethod
    def delete_dir(dir_path: str) -> None:
        """
        Deletes folder and everything inside it if it exists.
        :param dir_path: The path to the folder.
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def move_dir_contents(orig_path: str, new_path: str, delete_after_move: bool = False) -> None:
        """
        Moves the directory at the original path to the new path
        :param orig_path: the original path to move
        :param new_path: the new path to move the dir to
        :param delete_after_move: if True, deletes the original directory after moving all contents
        :return: None
        """
        FileUtilTest.create_dir_safely(new_path)
        for file in os.listdir(orig_path):
            file_path = os.path.join(orig_path, file)
            shutil.move(file_path, new_path)
        if delete_after_move:
            FileUtilTest.delete_dir(orig_path)

    @staticmethod
    def add_to_path(path: str, addition: str, index: int) -> str:
        """"
        Adds component to path at given index.
        :param path: The path to add component to.
        :param addition: The component to add to path.
        :param index: The index to add component in path.
        :return path with component added.
        """
        path = deepcopy(path)
        path_list = FileUtilTest.path_to_list(path)
        index = index if index >= 0 else len(path_list) + index + 1
        path_list.insert(index, addition)
        if os.path.isabs(path):
            path_list.insert(0, "/")
        return os.path.join(*path_list)

    @staticmethod
    def path_to_list(path: str) -> List[str]:
        """
        Creates list of folders and files in path.
        :param path: The path to split into components.
        :return: List of components creating path.
        """
        path = os.path.normpath(path)
        return [p for p in path.split(os.sep) if p != ""]

    @staticmethod
    def ls_dir(path: str, **kwargs):
        """
        Gets the directories at the current path
        :param path: Path to the directory
        :param kwargs: Additional parameters
        :return: The list of directories at the path
        """
        function_kwargs = {"add_base_path": True}
        function_kwargs.update(kwargs)
        return FileUtilTest.ls_filter(path, f=lambda f: os.path.isdir(f), **function_kwargs)

    @staticmethod
    def ls_filter(base_path: str, f: Callable[[str], bool] = None, ignore: List[str] = None, add_base_path: bool = False) -> List[str]:
        """
        List and filters files in path.
        :param base_path: The path to list its contents.
        :param f: The filtering function to select entities or not.
        :param ignore: List of files to ignored completely.
        :param add_base_path: Whether listed files should be complete paths.
        :return: List of files in path.
        """
        if f is None:
            f = lambda s: s
        if ignore is None:
            ignore = []
        results = os.listdir(base_path)
        results = list(filter(lambda p: p not in ignore, results))
        if add_base_path:
            results = list(map(lambda r: os.path.join(base_path, r), results))
        results = list(filter(lambda p: f(p), results))
        return results

    @staticmethod
    def split_base_path_and_filename(file_path: str) -> Tuple[str, str]:
        """
        Splits the filepath into base directory and the filename
        :param file_path: The path to the file
        :return: A tuple containing the base directory and the filename
        """
        return os.path.dirname(file_path), os.path.basename(file_path)

    @staticmethod
    def get_file_name(script_path: str, n_parents: int = 0, delimiter: str = "-"):
        """
        Returns the name of the file referenced in path.
        :param script_path: Path to script file whose name is returned.
        :param n_parents: The number of directories above file to include.
        :param delimiter: The delimiter to use if parents included.
        :return: The name of the script.
        """
        base_name, _ = os.path.splitext(script_path)
        components = []
        for i in range(n_parents + 1):  # file name + parents
            base_name, file_name = os.path.split(base_name)
            components.append(file_name)
        components.reverse()
        return delimiter.join(components)

    @staticmethod
    def find_all_file_paths_that_meet_condition(dir_path: str, condition: Callable = None) -> List[str]:
        """
        Reads all code files in directory with allowed extensions.
        :param dir_path: Path to directory where code files live
        :param condition: A callable that returns True if the filepath should be included
        :return: List containing all code file paths.
        """
        condition = condition if condition is not None else lambda x: True
        file_paths = []
        for subdir, dirs, files in os.walk(dir_path):
            for f in files:
                if condition(f):
                    file_paths.append(os.path.join(subdir, f))
        return file_paths


@dataclass
class ParamSpecsTest:
    param_names: Set[str]
    param_types: Dict[str, Union[Type]]
    has_kwargs: bool
    required_params: Set[str]
    name: str

    @staticmethod
    def create_from_method(method: Callable) -> "ParamSpecsTest":
        """
        Returns the param specs for the given method
        :param method: the method to create param specs for
        :return: the param specs
        """
        full_specs = getfullargspec(method)
        expected_param_names = full_specs.args
        expected_param_names.remove("self")

        param_names = set(copy(expected_param_names))
        type_hints = get_type_hints(method)
        param_types = {param: type_hints[param] if param in type_hints else None for param in param_names}

        expected_param_names.reverse()
        required_params = {param for i, param in enumerate(expected_param_names)
                           if not full_specs.defaults or i >= len(full_specs.defaults)}

        return ParamSpecsTest(name=str(method), param_names=param_names, param_types=param_types,
                              required_params=required_params, has_kwargs=full_specs.varkw is not None)

    def assert_definition(self, definition: Dict) -> None:
        """
        Asserts that there are no missing or unexpected params for the method represented by the given param specs
        :param definition: the dictionary of parameter name to value mappings to check
        :return: None (raises an exception if there are missing params)
        """
        missing_params = self.get_any_missing_required_params(definition)
        if len(missing_params) >= 1:
            raise TypeError("%s is missing required arguments: %s" % (self.name, missing_params))
        self.assert_no_unexpected_params(definition)

    def assert_no_unexpected_params(self, definition: Dict) -> None:
        """
        Asserts that there are no unexpected params for the method represented by the given param specs
        :param definition: the dictionary of parameter name to value mappings to check
        :return: None (raises an exception if there are unexpected params)
        """
        extra_params = self.get_any_additional_params(definition)
        if len(extra_params) >= 1 and not self.has_kwargs:
            raise TypeError("%s received unexpected arguments: %s" % (self.name, extra_params))

    def get_any_missing_required_params(self, param_dict: Dict) -> Set[str]:
        """
        Gets any missing params for the given param specs that are not supplied in the parameter dictionary
        :param param_dict: the dictionary of parameter name to value mappings to check
        :return: a set of any missing required parameters
        """
        return set(self.required_params).difference(set(param_dict.keys()))

    def get_any_additional_params(self, param_dict: Dict) -> Set[str]:
        """
        Gets any additional params for the given param specs that are supplied in the parameter dictionary
        :param param_dict: the dictionary of parameter name to value mappings to check
        :return: a set of any additional parameters
        """
        return set(param_dict.keys()).difference(self.param_names)


test = 1 + 2
func = lambda x: x + 1
new_test = func(test)
if new_test < test:
    pass
