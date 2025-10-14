import collections
import os
from enum import Enum, EnumMeta
from typing import Any, Dict

from tqdm import tqdm
from yaml.constructor import ConstructorError
from yaml.dumper import Dumper
from yaml.loader import SafeLoader
from yaml.nodes import MappingNode, Node

from gen_common.constants.symbol_constants import COLON
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.file_util import FileUtil
from gen_common.util.param_specs import ParamSpecs
from gen_common.util.reflection_util import ReflectionUtil


class CustomLoader(SafeLoader):
    __top_level_reached = False
    __time_to_load = {}

    def construct_custom(self, _, node: Node) -> Any:
        """
        Constructs (mostly) any object that is not known to the yaml parser already
        :param _: unused, left for api
        :param node: The yaml node being parsed
        :return: The created object
        """
        try:
            # start = timeit.timeit()
            class_path = node.tag.split(COLON)[-1]
            cls = ReflectionUtil.get_cls_from_path(class_path)
            if ReflectionUtil.is_function(cls) or "builtins" in class_path and "Exception" not in class_path:
                return cls
            if isinstance(cls, EnumMeta):
                if isinstance(node.value, str):
                    return cls[node.value]
                return self._create_enum_from_meta(cls, node)
            if ReflectionUtil.is_instance_or_subclass(cls, Exception):
                return cls(node.value[0].value)
            deep = hasattr(cls, '__setstate__')
            state = self.construct_mapping(node, deep=True)
            use_init = False
            if hasattr(cls, '__init__'):
                param_specs = ParamSpecs.create_from_method(cls.__init__)
                init_params = {name: val for name, val in state.items() if name in param_specs.param_names}
                try:
                    data = cls(**init_params)
                    use_init = True
                except Exception as e:
                    pass
            if not use_init:
                data = cls.__new__(cls)
            if 'dictitems' in state:
                data.update(state['dictitems'])
            elif deep:
                data.__setstate__(state)
            else:
                data.__dict__.update(state)
            if hasattr(data, "from_yaml"):
                data.from_yaml()
            # end = timeit.timeit()
            # self.__time_to_load[class_path] = max(end - start, self.__time_to_load.get(class_path, 0))
            return data
        except Exception as e:
            logger.error(f"Problem loading node {node.tag}")
            raise e

    def _create_enum_from_meta(self, enum_meta: EnumMeta, node: Node) -> Enum:
        """
        Creates an enum from its meta obj
        :param enum_meta: The meta obj for an enum
        :param node: The yaml node containing the enum's value
        :return: The enum with the value contained in the node
        """
        value = self.construct_object(node.value[0])
        find_enum = [e for e in enum_meta if e.value == value]
        if len(find_enum) > 0:
            return find_enum.pop()

    def construct_object(self, node, deep=False) -> Any:
        """
        Overrides the normal yaml loader to make custom objects
        :param node: The node being parsed
        :param deep: Used in the yaml parser
        :return: The constructed object
        """
        if node.tag not in self.yaml_constructors:
            self.yaml_constructors[node.tag] = self.construct_custom
        return super().construct_object(node, deep)

    def construct_mapping(self, node, deep=False):
        """
        Overwritten to allow tqdm on top level
        :param node: Yaml Node
        :param deep: from yaml API
        :return: The constructed mapping
        """
        if not self.__top_level_reached:
            return self._run_top_level(node, deep)
        return super().construct_mapping(node, deep)

    def _run_top_level(self, node, deep=False) -> Dict:
        """
        Copied from BaseConstructor to allow tqdm
        :param node: Yaml Node
        :param deep: from yaml API
        :return: The constructed mapping for top level
        """
        self.__top_level_reached = True
        if isinstance(node, MappingNode):
            self.flatten_mapping(node)
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                                   "expected a mapping node, but found %s" % node.concept_id,
                                   node.start_mark)
        mapping = {}
        for key_node, value_node in tqdm(node.value, desc="Loading objects from yaml"):
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise ConstructorError("while constructing a mapping", node.start_mark,
                                       "found unhashable key", key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


class CustomDumper(Dumper):
    _time_to_save = {}

    def represent_data(self, data) -> Node:
        """
        Represent data in a yaml form
        :param data: The data to represent
        :return: The data in a yaml form (node)
        """
        if hasattr(data, "to_yaml"):
            try:
                converted_data = data.to_yaml()
                if type(data) != type(converted_data):
                    node = super().represent_data(converted_data)
                    node.tag = self.get_original_node_tag(data)
                    return node
                data = converted_data
            except Exception:
                pass
        elif hasattr(data, "item"):
            data = data.item()
        node = super().represent_data(data)
        return node

    def get_original_node_tag(self, data) -> "str":
        """
        Gets the tag that yaml would typical assign the data
        :param data: The original data
        :return: The tag that yaml would typical assign the data
        """
        orig_node = self.represent_object(data)
        return orig_node.tag


class YamlUtil:

    @staticmethod
    def read(path2yaml: str) -> Dict:
        """
        Reads a yaml file into a python obj
        :param path2yaml: The path to the yaml file
        :return: The file as a python obj
        """
        return FileUtil.read_yaml(path2yaml, loader=CustomLoader)

    @staticmethod
    def write(content: Any, output_path: str) -> None:
        """
        Writes the yaml file.
        :param content: The content as a python obj
        :param output_path: The path to save to
        :return: None
        """
        export_dir = FileUtil.get_directory_path(output_path)
        content = YamlUtil.convert_content_to_yaml_serializable(content, export_dir)
        FileUtil.write_yaml(content, output_path, dumper=CustomDumper)

    @staticmethod
    def convert_content_to_yaml_serializable(content: Any, export_dir: str, key: str = None) -> Any:
        """
        Converts the content to yaml serializable if to_yaml is defined
        :param content: The content to convert
        :param export_dir: The directory to which the yaml will be exported
        :param key: If part of a dictionary, the key the content is mapped to
        :return: Content converted to yaml serializable if to_yaml is defined
        """
        if isinstance(content, dict):
            converted = {k: YamlUtil.convert_content_to_yaml_serializable(v, export_dir, key=k) for k, v in content.items()}
        elif isinstance(content, list) or isinstance(content, set):
            converted = [YamlUtil.convert_content_to_yaml_serializable(v, export_dir) for v in content]
        elif hasattr(content, "to_yaml"):
            if key is not None:
                export_dir = os.path.join(export_dir, str(key))
            yamified_content = content.to_yaml(export_path=export_dir)
            return yamified_content
        else:
            return content

        if converted.__class__ != content.__class__:
            converted = content.__class__(converted)
        return converted
