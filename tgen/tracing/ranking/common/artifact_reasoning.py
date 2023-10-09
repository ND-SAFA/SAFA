from typing import Dict, Any, Optional

from tgen.common.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.common.constants.ranking_constants import RANKING_ID_TAG, RANKING_SCORE_TAG, RANKING_MAX_SCORE, RANKING_ARTIFACT_TAG, \
    JUSTIFICATION_TAG, RANKING_MIN_SCORE
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.math_util import MathUtil
from tgen.data.keys.structure_keys import ArtifactKeys


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict, require_id: bool = True):
        """
        Stores the reasoning of the LLM for each artifact
        :param artifact_dict: Contains the reasoning of the LLM for each artifact
        """
        if require_id:
            JsonUtil.require_properties(artifact_dict, [ArtifactKeys.ID.value])
        self.index = self.get_attr(RANKING_ID_TAG, artifact_dict, pop=True)
        self.score = MathUtil.normalize_val(self.get_attr(RANKING_SCORE_TAG, artifact_dict, 0.0, pop=True),
                                            max_val=RANKING_MAX_SCORE, min_val=RANKING_MIN_SCORE)
        self.explanation = self.construct_explanation(artifact_dict)
        self.artifact_id = None

    def construct_explanation(self, explanation_parts: Dict) -> str:
        """
        Constructs the explanation from its parts
        :param explanation_parts: Dictionary mapping explanation part name and content
        :return: The explanation as a str
        """
        explanation_values = {name: ArtifactReasoning.get_attr(name, explanation_parts)
                              for name in explanation_parts.keys() if name != RANKING_ARTIFACT_TAG}
        formatted_values = [self.format_for_explanation(val, self.score, remove_score=name == JUSTIFICATION_TAG)
                            for name, val in explanation_values.items() if val]
        return NEW_LINE.join(formatted_values)

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

    @staticmethod
    def format_for_explanation(explanation_part: str, score: float, remove_score: bool) -> Optional[str]:
        """
        Formats the explanation portion of the reasoning
        :param explanation_part: The part of the explanation to format
        :param score: The score given to the artifact
        :param remove_score: If True, removes the score from the explanation
        :return: The formatted explanation part
        """
        if not explanation_part:
            return
        lines = explanation_part.strip().split(NEW_LINE)
        if remove_score:
            lines = [line for line in lines if str(score) not in line]
        return EMPTY_STRING.join(lines)
