from copy import deepcopy

from tgen.common.constants.project_summary_constants import PROJECT_SUMMARY_TAGS, PS_DATA_FLOW_TITLE, PS_ENTITIES_TITLE, \
    PS_FEATURE_TITLE, \
    PS_NOTES_TAG, \
    PS_OVERVIEW_TITLE, PS_SUBSYSTEM_TITLE, MULTI_LINE_ITEMS
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.summarizer.summary import Summary

MOCK_PS_RES_MAP = {
    PS_OVERVIEW_TITLE: "project_overview",
    PS_FEATURE_TITLE: "project_features",
    PS_ENTITIES_TITLE: "project_entities",
    PS_SUBSYSTEM_TITLE: "project_subsytem",
    PS_DATA_FLOW_TITLE: "project_data_flow"
}


SECTION_TAG_TO_TILE = {
    v: k for k, v in PROJECT_SUMMARY_TAGS.items()
}


TEST_PROJECT_SUMMARY = Summary({title: EnumDict({"chunks": ["summary of project"], "title": title})
                                for title in MOCK_PS_RES_MAP.keys()})


def create(title: str, body_prefix: str = None, tag: str = None):
    if body_prefix is None:
        body_prefix = ""
    tag = PROJECT_SUMMARY_TAGS[title] if not tag else tag
    body = MOCK_PS_RES_MAP.get(title, f"project_{title.lower()}")
    if title in MULTI_LINE_ITEMS:
        body_prefix = PromptUtil.create_xml("name", body_prefix if body_prefix else "name")
        body = PromptUtil.create_xml("descr", body)
    r = ""
    r += PromptUtil.create_xml(PS_NOTES_TAG, "notes")
    r += PromptUtil.create_xml(tag, f"{body_prefix}{body}")
    return r


class MockResponses:
    project_title_to_response = {title: create(title) for title in MOCK_PS_RES_MAP.keys()}
    project_summary_responses = [project_title_to_response[PS_FEATURE_TITLE],
                                 project_title_to_response[PS_ENTITIES_TITLE],
                                 project_title_to_response[PS_SUBSYSTEM_TITLE],
                                 project_title_to_response[PS_DATA_FLOW_TITLE],
                                 project_title_to_response[PS_OVERVIEW_TITLE]]

    def __getattr__(self, item: str):
        """
        Returns a copy of the requested attribute.
        :param item: The name of the attribute.
        :return: The value of the attribute.
        """
        item_value = super().__getattribute__(item)
        return deepcopy(item_value)
