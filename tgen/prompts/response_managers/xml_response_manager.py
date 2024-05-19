from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.response_managers.abstract_response_manager import AbstractResponseManager


@dataclass
class XMLResponseManager(AbstractResponseManager):

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        if not self.response_tag:
            return {}
        output = {}
        if isinstance(self.response_tag, dict):
            for parent, child_tags in self.response_tag.items():
                values = LLMResponseUtil.parse(response, parent, is_nested=True, raise_exception=parent in self.required_tag_ids,
                                               is_optional=parent in self.optional_tag_ids)
                tags = child_tags + [parent]
                values = [{self._tag2id[c_tag]: val.get(c_tag, None) for c_tag in tags if c_tag in val or c_tag != parent}
                          for val in values]
                output[self._tag2id[parent]] = values
        else:
            tags, _ = self._convert2list(self.response_tag)
            for tag in tags:
                tag_id = self._tag2id[tag]
                parsed = LLMResponseUtil.parse(response, tag, is_nested=False, raise_exception=tag in self.required_tag_ids,
                                               is_optional=tag in self.optional_tag_ids)
                output[tag_id] = parsed if len(parsed) > 0 else [None]
        formatted_output = self._format_response(output)
        return formatted_output

    def _collect_all_tags(self) -> List[str]:
        """
        Collects all response tags used.
        :return: a list of all response tags that are used.
        """
        all_tags = []
        if isinstance(self.response_tag, str):
            all_tags.append(self.response_tag)
        elif isinstance(self.response_tag, list):
            all_tags.extend(self.response_tag)
        else:
            for tag, children in self.response_tag.items():
                all_tags.append(tag)
                all_tags.extend(children)
        return all_tags

    def _get_response_instructions_format_params(self) -> Tuple[List, Dict]:
        """
        Formats all tags to xml for the args and kwargs needed for response instructions.
        :return: The args and kwargs needed for the response instructions format.
        """
        args = [PromptUtil.create_xml(tag_name=tag) for tag in self.get_all_tag_ids()]
        kwargs = {id_: PromptUtil.create_xml(tag_name=tag) for id_, tag in self.id2tag.items()}
        return args, kwargs
