from typing import Callable, Dict


class Artifact:
    """
    Data structure representing artifact in project.
    """

    def __init__(self, id_: str, token: str):
        """
        Represents an artifact (i.e. source and target)
        :param id_: artifact id
        :param token: artifact token
        """
        self.id = id_
        self.token = token

    def get_feature(self, feature_func: Callable) -> Dict:
        """
        Calls the feature function to get the artifact feature
        :return: feature name, value mappings
        """
        return feature_func(text=self.token)

    def __hash__(self):
        return hash(self.id)
