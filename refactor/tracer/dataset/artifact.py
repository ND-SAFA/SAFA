from typing import Callable, Dict


class Artifact:
    """
    Data structure representing artifact in project.
    """

    def __init__(self, id_: str, token: str, feature_func: Callable):
        """
        Represents an artifact (i.e. source and target)
        :param id_: artifact id
        :param token: artifact token
        :param feature_func: function from which the artifact features can be generated
        """
        self.id = id_
        self.token = token
        self.__feature_func = feature_func  # delay execution in case not needed
        self.__feature = None
        self.embedding = None  # TODO: When is this used?

    def get_feature(self, feature_func: Callable) -> Dict:
        """
        Calls the feature function to get the artifact feature
        :return: feature name, value mappings
        """
        return feature_func(text=self.token)

    def __hash__(self):
        return hash(self.id)
