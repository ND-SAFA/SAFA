from collections.abc import Callable
from typing import Dict, Tuple

from trace.data.artifact import Artifact


class TraceLink:
    """
    Data structure representing link between source and target artifact.
    """

    def __init__(self, source: Artifact, target: Artifact, feature_func: Callable, is_true_link: bool = False):
        """
        Represents a link between source and target
        :param source: source artifact
        :param target: target artifact
        :param feature_func: function from which the link feature can be generated
        :param is_true_link: if True, represents a positive link
        """
        self.source = source
        self.target = target
        self.id = self.generate_link_id(self.source.id, self.target.id)
        self.is_true_link = is_true_link
        self.__feature_func = feature_func  # delay execution in case not needed
        self.__feature = None

    def get_feature(self) -> Dict:
        """
         Calls the feature function to get the link feature
         :return: a dictionary of features
         """
        if self.__feature is None:
            self.__feature = self.__feature_func(text=self.source.token,
                                                 text_pair=self.target.token,
                                                 return_token_type_ids=True,
                                                 add_special_tokens=True)
        return self.__feature

    def get_source_target_ids(self) -> Tuple[str, str]:
        """
        Gets the ids of the source and target
        :return: the ids of the source and target
        """
        return self.source.id, self.target.id

    @staticmethod
    def generate_link_id(source_id: str, target_id: str) -> int:
        """
        Generates a unique id for a source, target link
        :param source_id: id of source artifact
        :param target_id: id of target artifact
        :return: the link id
        """
        return hash(source_id) + hash(target_id)

    def __hash__(self):
        return self.id
