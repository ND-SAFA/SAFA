import html
import logging
import os
import re
from typing import Any, Dict, List, Set, Tuple, Union

import numpy as np
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

from common_resources.llm.llm_responses import GenerationResponse, SupportedLLMResponses
from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.tools.util.yaml_util import YamlUtil


class LLMResponseUtil:

    @staticmethod
    def extract_predictions_from_response(predictions: Union[np.ndarray, Tuple[np.ndarray], List],
                                          response_prompt_ids: Union[Set, str] = None,
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
    def parse(res: str, tag_name: str, is_nested: bool = False, is_optional: bool = False,
              raise_exception: bool = False, return_res_on_failure: bool = False) -> List[Union[str, Dict]]:
        """
        Parses the LLM response for the given html tags
        :param res: The LLM response
        :param tag_name: The name of the tag to find
        :param is_nested: If True, the response contains nested tags so all Tag objects are returned, else just the single content
        :param is_optional: If True, does not raise an exception if the parsing fails.
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
        except Exception as e:
            if not is_optional:
                error = f"{NEW_LINE}Unable to parse {tag_name}"
                logger.log_without_spam(level=logging.ERROR, msg=error)
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
    def reload_responses(load_path: str) -> Union[GenerationResponse, List]:
        """
        Reloads existing responses if they exist and returns
        :param load_path:
        :return:
        """
        responses_for_retry = None
        if FileUtil.safely_check_path_exists(load_path):
            logger.info(f"IMPORTANT!!! Loading previous LLM responses from {load_path}")
            res = YamlUtil.read(load_path)
            failed_responses = LLMResponseUtil.get_failed_responses(res)
            if len(failed_responses) > 0:
                responses_for_retry = LLMResponseUtil.get_batch_responses(res)
            return responses_for_retry if responses_for_retry else res

    @staticmethod
    def save_responses(responses: GenerationResponse, save_path: str) -> bool:
        """
        Saves the model's responses.
        :param responses: The responses to save.
        :param save_path: The path to save responses to.
        :return: Whether the save was successful or not.
        """
        if save_path:
            logger.info(f"Saved LLM responses to {save_path}")
            FileUtil.create_dir_safely(save_path)
            YamlUtil.write(responses, save_path)
            return True
        return False

    @staticmethod
    def get_failed_responses(res: SupportedLLMResponses, raise_exception: bool = False) -> List[Exception]:
        """
        Gets failed responses from the response.
        :param res: The LLM Response.
        :param raise_exception: If True, raises an exception if there are failed responses.
        :return: A list of failed responses.
        """
        batch_responses = LLMResponseUtil.get_batch_responses(res)
        failed_responses = [r for r in batch_responses if isinstance(r, Exception)]
        if raise_exception and len(failed_responses) > 0:
            raise Exception(failed_responses[0])
        return failed_responses

    @staticmethod
    def get_batch_responses(res: SupportedLLMResponses) -> List[str]:
        """
        Gets batch responses from the response.
        :param res: The LLM Response.
        :return: Batch responses.
        """
        batch_responses = res.batch_responses if isinstance(res, GenerationResponse) else [r.text for r in res.batch_responses]
        return batch_responses

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
        :return: The full path to save and load to
        """
        filename = FileUtil.add_ext(filename, FileUtil.YAML_EXT)
        path = os.path.join(base_dir, "responses", filename)
        return path

    @staticmethod
    def get_non_empty_responses(response_dict: Dict, return_first: bool = True) -> Any:
        """
        Extracts only the prompt ids and tags that have responses.
        :param response_dict: The original parsed response dict.
        :param return_first: If True, returns the first non-empty response.
        :return: Only the prompt ids and tags that have responses.
        """
        responses = []
        for k, v in response_dict.items():
            if v:
                if isinstance(v, dict):
                    responses.extend(LLMResponseUtil.get_non_empty_responses(v))
                else:
                    responses.append(v)
        return responses[0] if return_first and len(responses) > 0 else responses
