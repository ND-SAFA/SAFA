import html
import os
import re
from typing import Dict, List, Set, Union

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.path_constants import RESPONSES_DIRNAME
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.core.trace_output.stage_eval import TracePredictions


class LLMResponseUtil:

    @staticmethod
    def extract_predictions_from_response(predictions: TracePredictions, response_prompt_ids: Union[Set, str] = None,
                                          tags_for_response: Union[Set, str] = None, return_first: bool = False):
        """
        Extracts the desired predictions from the llm output
        :param predictions: The predictions from the LLMTrainer
        :param response_prompt_ids: The prompt id to extract from predictions
        :param tags_for_response: The tag to extract from predictions
        :param return_first: If True, returns the first item from each list of parsed tags (often there is only one per tag)
        :return: The model predictions
        """
        response_prompt_ids = {response_prompt_ids} if not isinstance(response_prompt_ids, set) else response_prompt_ids
        if response_prompt_ids:
            predictions = [DictUtil.combine_child_dicts(p, response_prompt_ids) for p in predictions]
            if tags_for_response:
                predictions = [DictUtil.filter_dict_keys(p, keys2keep=tags_for_response) if isinstance(tags_for_response, set)
                               else p[tags_for_response] for p in predictions]
                if return_first:
                    if isinstance(predictions[0], dict):
                        predictions = [{key: value[0] if isinstance(value, list) else value for key, value in p.items()}
                                       for p in predictions]
                    else:
                        predictions = [p[0] for p in predictions]
        return predictions

    @staticmethod
    def parse(res: str, tag_name: str, is_nested: bool = False, raise_exception: bool = False, return_res_on_failure: bool = False) -> \
            List[Union[str, Dict]]:
        """
        Parses the LLM response for the given html tags
        :param res: The LLM response
        :param tag_name: The name of the tag to find
        :param is_nested: If True, the response contains nested tags so all Tag objects are returned, else just the single content
        :param raise_exception: if True, raises an exception if parsing fails
        :param return_res_on_failure: Whether to return original response on failure.
        :return: Either a list of tags (if nested) or the content inside the tag (not nested)
        """
        soup = BeautifulSoup(res, features="lxml")

        try:
            assert tag_name in res, f"Missing expected tag {tag_name}"
            tags = soup.findAll(tag_name)
            if is_nested:
                content = [LLMResponseUtil._parse_children(tag) for tag in tags]
            else:
                content = []
                for tag in tags:
                    c = LLMResponseUtil._get_content(tag)
                    if c:
                        content.append(c)
            assert len(content) > 0, f"Found no tags ({tag_name}) in:\n{res}"
        except Exception:
            error = f"Unable to parse {tag_name}"
            logger.warning(error)
            if raise_exception:
                raise Exception(error)
            content = [res] if return_res_on_failure else []
        return [html.unescape(c) for c in content]

    @staticmethod
    def _parse_children(tag: Tag) -> Dict[str, List]:
        """
        Parses all children tags in the given tag
        :param tag: The parent tag
        :return: The children of the tag
        """
        children = {}
        if isinstance(tag, str):
            return tag
        for child in tag.children:
            if isinstance(child, Tag) and child.contents is not None and len(child.contents) > 0:
                tag_name = child.name
                content = child.contents[0]
            elif isinstance(child, NavigableString):
                tag_name = tag.name
                content = child
                if not PromptUtil.strip_new_lines_and_extra_space(content):
                    continue
            else:
                continue
            if tag_name not in children:
                children[tag_name] = []
            children[tag_name].append(content)
        return children

    @staticmethod
    def _get_content(tag: Union[str, Tag]) -> str:
        """
        Gets the content from the tag.
        :param tag: The tag expected to contain LLM response.
        :return: The content
        """
        if isinstance(tag, str):
            return tag
        if isinstance(tag, Tag):
            contents = []
            for c in tag.contents:
                content = LLMResponseUtil._get_content(c)
                contents.append(content)
            return EMPTY_STRING.join(contents)

    @staticmethod
    def extract_labels(r: str, labels2props: Union[Dict, List]) -> Dict:
        """
        Extracts XML labels from response.
        :param r: The text response.
        :param labels2props: Dictionary mapping XML property name to export prop name.
        :return: Dictionary of prop names to values.
        """
        if isinstance(labels2props, list):
            labels2props = {label: label for label in labels2props}
        props = {}
        for tag, prop in labels2props.items():
            try:
                prop_value = LLMResponseUtil.parse(r, tag, raise_exception=True)
            except Exception:
                prop_value = []
            props[prop] = prop_value
        return props

    @staticmethod
    def strip_non_digits_and_periods(string: str):
        """
        Removes all characters except digits and periods.
        :param string: The str to strip.
        :return: The stripped string.
        """
        pattern = r'[^0-9.]'
        return re.sub(pattern, '', string)

    @staticmethod
    def generate_response_save_and_load_path(base_dir: str, filename: str) -> str:
        """
        Generates a save and load path for responses using a given base directory and a filename
        :param base_dir: The base directory to save/load to
        :param filename: The base filename to use
        :param create: If True, creates the directory as well
        :return: The full path to save and load to
        """
        filename = FileUtil.add_ext(filename, FileUtil.YAML_EXT)
        path = os.path.join(base_dir, RESPONSES_DIRNAME, filename)
        return path
