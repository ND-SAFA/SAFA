from typing import Any, Dict, Optional, Tuple

from gen_common.constants.ranking_constants import JUSTIFICATION_TAG, RANKING_ARTIFACT_TAG, RANKING_ID_TAG, \
    RANKING_MAX_SCORE, \
    RANKING_MIN_SCORE, RANKING_SCORE_TAG
from gen_common.constants.symbol_constants import COMMA, EMPTY_STRING, NEW_LINE, PERIOD, SPACE
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.util.json_util import JsonUtil
from gen_common.util.math_util import MathUtil
from gen_common.util.prompt_util import PromptUtil
from gen_common.util.str_util import StrUtil


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict = None,
                 index: int = None,
                 artifact_id: str = None,
                 score: float = None,
                 explanation: str = EMPTY_STRING,
                 require_id: bool = True):
        """
        Stores the reasoning of the LLM for each artifact
        :param index: The index associated with overall artifacts.
        :param artifact_dict: Contains the reasoning of the LLM for each artifact
        :param artifact_id: The id of the artifact
        :param score: The score given to the artifact evaluating relationship to parent
        :param explanation: The explanation of why that score was given
        :param require_id: Whether to require artifact ids.
        """
        self.artifact_id = artifact_id
        if artifact_dict:
            if require_id:
                JsonUtil.require_properties(artifact_dict, [ArtifactKeys.ID.value])
            index, score, explanation = self._extract_properties_from_artifact_dict(artifact_dict)
        self.index = index
        self.score = score
        self.explanation = explanation

    def _extract_properties_from_artifact_dict(self, artifact_dict: Dict) -> Tuple[int, float, str]:
        """
        Extracts the necessary attributes from the dictionary containing parsed artifct from LLM
        :param artifact_dict:
        :return:
        """
        index = self.get_attr(RANKING_ID_TAG, artifact_dict, pop=True)
        score = self.get_attr(RANKING_SCORE_TAG, artifact_dict, pop=True)
        explanation = self.construct_explanation(artifact_dict)
        if score:
            score = MathUtil.normalize_val(score, max_val=RANKING_MAX_SCORE, min_val=RANKING_MIN_SCORE)
        return index, score, explanation

    def construct_explanation(self, explanation_parts: Dict) -> str:
        """
        Constructs the explanation from its parts
        :param explanation_parts: Dictionary mapping explanation part name and content
        :return: The explanation as a str
        """
        explanation_values = {name: ArtifactReasoning.get_attr(name, explanation_parts)
                              for name in explanation_parts.keys() if name != RANKING_ARTIFACT_TAG}
        explanation_values = {name: val for name, val in explanation_values.items() if val}  # remove empty

        summary = self.format_for_explanation(explanation_values.pop(JUSTIFICATION_TAG), remove_score=True,
                                              bold=True, as_bullet=False) if JUSTIFICATION_TAG in explanation_values else None

        formatted_values = [self.format_for_explanation(val) for i, val in enumerate(explanation_values.values())]
        if summary and len(summary.strip()) > 5:
            formatted_values = [PromptUtil.as_blockquote(summary), PromptUtil.markdown_divider()] + formatted_values
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
    def format_for_explanation(explanation_part: str, remove_score: bool = False,
                               header: str = EMPTY_STRING, bold: bool = False, as_bullet: bool = True) -> Optional[str]:
        """
        Formats the explanation portion of the reasoning
        :param explanation_part: The part of the explanation to format
        :param remove_score: If True, removes the score from the explanation (in the case the model mistakenly printed it)
        :param header: If provided, the header will be added to the explanation in markdown
        :param bold: If True, bolds the explanation part
        :param as_bullet: If True, creates a bullet for the explanation part
        :return: The formatted explanation part
        """
        if not explanation_part:
            return
        explanation_part = explanation_part.strip()
        if remove_score:
            lines = StrUtil.split_sentences_by_punctuation(explanation_part, PERIOD)
            lines[0] = StrUtil.remove_floats(lines[0])  # just remove the score if its the first sentence
            # remove the whole sentence if it is later in the paragraph
            lines = [line for line in lines if not ArtifactReasoning._contains_possible_score(line) and len(line.strip()) > 1]
            explanation_part = f"{PERIOD}{SPACE}".join(lines)
        if bold:
            explanation_part = PromptUtil.as_markdown_bold(explanation_part)
        if as_bullet:
            explanation_part = PromptUtil.as_bullet_point(explanation_part)
        if header:
            explanation_part = ArtifactReasoning._add_header_to_explanation(header, explanation_part)
        return explanation_part

    @staticmethod
    def _contains_possible_score(line: str) -> bool:
        """
        Checks if the line possible contains a score
        :param line: The line to check
        :return: True if it likely contains a score else False
        """
        line_parts = StrUtil.split_sentences_by_punctuation(line, COMMA)
        contains_score = [l for l in line_parts if len(StrUtil.find_floats(l)) > 0]
        return len(contains_score) > 0

    @staticmethod
    def _add_header_to_explanation(header: str, explanation: str) -> str:
        """
        Adds a header to the explanations
        :param header: The header for the explanations
        :param explanation: The explanation
        :return: The full string with header prepended
        """
        formatted = f"{PromptUtil.as_markdown_header(header, level=4)}{NEW_LINE}{explanation}"
        return formatted
