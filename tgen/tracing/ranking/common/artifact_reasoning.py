from typing import Dict, Any

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.tracing.ranking_constants import RANKING_ID_TAG, RANKING_SCORE_TAG, RANKING_MAX_SCORE, RANKING_ARTIFACT_TAG
from tgen.common.util.json_util import JsonUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict, require_id: bool = True):
        """
        Stores the reasoning of the LLM for each artifact
        :param artifact_dict: Contains the reasoning of the LLM for each artifact
        """
        if require_id:
            JsonUtil.require_properties(artifact_dict, [ArtifactKeys.ID.value])
        self.index = self.get_attr(RANKING_ID_TAG, artifact_dict, pop=True)
        self.score = self.get_attr(RANKING_SCORE_TAG, artifact_dict, 0.0, pop=True) / RANKING_MAX_SCORE
        self.explanation = self.construct_explanation(artifact_dict)
        self.artifact_id = None

    @staticmethod
    def construct_explanation(explanation_parts: Dict) -> str:
        """
        Constructs the explanation from its parts
        :param explanation_parts: Dictionary mapping explanation part name and content
        :return: The explanation as a str
        """
        explanation_values = [ArtifactReasoning.get_attr(name, explanation_parts) for name in explanation_parts.keys()
                              if name != RANKING_ARTIFACT_TAG]
        return NEW_LINE.join([v for v in explanation_values if v])

    @staticmethod
    def get_attr(attr_name: str, artifact_dict: Dict, default: Any = None, expected_list: bool = False, pop: bool = False) -> Any:
        """
        Gets an attributes from the artifact dict
        :param attr_name: The key to retrieve
        :param artifact_dict: The artifact dict to retrieve it from
        :param default: Default value if it doesnt exist
        :param expected_list: If True, the value of the attr is expected to be a list
        :param pop: If True, pops the value during retrieval
        :return: The value of the attr
        """
        if pop:
            val = artifact_dict.pop(attr_name) if attr_name in artifact_dict else default
        else:
            val = artifact_dict.get(attr_name, default)
        if isinstance(val, list) and not expected_list:
            val = val[0] if val else default
        return val
