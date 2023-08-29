from tgen.common.constants.project_summary_constants import PROJECT_SUMMARY_TAGS, PS_DATA_FLOW_TITLE, PS_ENTITIES_TITLE, \
    PS_FEATURE_TITLE, \
    PS_NOTES_TAG, \
    PS_OVERVIEW_TITLE, PS_SUBSYSTEM_TITLE
from tgen.common.util.prompt_util import PromptUtil

MOCK_PS_RES_MAP = {
    PS_OVERVIEW_TITLE: "project_overview",
    PS_FEATURE_TITLE: "project_features",
    PS_ENTITIES_TITLE: "project_entities",
    PS_SUBSYSTEM_TITLE: "project_subsytem",
    PS_DATA_FLOW_TITLE: "project_flow"
}


def create(title: str, body_prefix: str = None):
    if body_prefix is None:
        body_prefix = ""
    tag = PROJECT_SUMMARY_TAGS[title]
    body = MOCK_PS_RES_MAP[title]
    r = ""
    r += PromptUtil.create_xml(PS_NOTES_TAG, "notes")
    r += PromptUtil.create_xml(tag, f"{body_prefix}{body}")
    return r


class MockResponses:
    project_overview = create(PS_OVERVIEW_TITLE)
    project_features = create(PS_FEATURE_TITLE)
    project_entities = create(PS_ENTITIES_TITLE)
    project_subsytem = create(PS_SUBSYSTEM_TITLE)
    project_flow = create(PS_DATA_FLOW_TITLE)
    project_summary_responses = [project_features,
                                 project_entities,
                                 project_subsytem,
                                 project_flow,
                                 project_overview]
