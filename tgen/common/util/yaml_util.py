from typing import Dict
from yaml.loader import SafeLoader

from tgen.common.util.file_util import FileUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.constants.deliminator_constants import COLON


class CustomLoader(SafeLoader):

    def construct_custom(self, loader, node):
        class_path = node.tag.split(COLON)[-1]
        cls = ReflectionUtil.get_cls_from_path(class_path)
        data = cls.__new__(cls)

        if hasattr(data, '__setstate__'):
            state = self.construct_mapping(node, deep=True)
            data.__setstate__(state)
        else:
            state = self.construct_mapping(node)
            data.__dict__.update(state)
        return data

    def construct_object(self, node, deep=False):
        if node.tag not in self.yaml_constructors:
            self.yaml_constructors[node.tag] = self.construct_custom
        return super().construct_object(node, deep)


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
    def write(content: Dict, output_path: str) -> None:
        """
        Writes the yaml file
        :param content: The content as a python obj
        :param output_path: The path to save to
        :return: None
        """
        FileUtil.write_yaml(content, output_path)
