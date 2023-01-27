from collections.abc import Callable
from typing import Dict

from data.tree.artifact import Artifact
from util.base_object import BaseObject


class TraceLink(BaseObject):
    """
    Data structure representing link between source and target artifact.
    """

    def __init__(self, source: Artifact, target: Artifact, is_true_link: bool = False):
        """
        Represents a link between source and target
        :param source: source artifact
        :param target: target artifact
        :param is_true_link: if True, represents a positive link
        """
        self.source = source
        self.target = target
        self.id = self.generate_link_id(self.source.id, self.target.id)
        self.is_true_link = is_true_link

    def get_label(self) -> int:
        """
        Gets the links label (0 if negative link, 1 if positive)
        :return: the link label
        """
        return int(self.is_true_link)

    def get_feature(self, feature_func: Callable) -> Dict:
        """
         Calls the feature function to get the link feature
         :return: a dictionary of features
         """
        return feature_func(text=self.source.token,
                            text_pair=self.target.token,
                            return_token_type_ids=True,
                            add_special_tokens=True)

    @staticmethod
    def generate_link_id(source_id: str, target_id: str) -> int:
        """
        Generates a unique id for a source, target link
        :param source_id: id of source artifact
        :param target_id: id of target artifact
        :return: the link id
        """
        return hash(str(hash(source_id)) + "-" + str(hash(target_id)))

    def __hash__(self):
        return self.id
