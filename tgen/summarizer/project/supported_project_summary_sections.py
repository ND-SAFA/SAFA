from tgen.common.constants.project_summary_constants import PS_DATA_FLOW_TITLE, PS_ENTITIES_TITLE, PS_FEATURE_TITLE, PS_OVERVIEW_TITLE, \
    PS_SUBSYSTEM_TITLE
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts

PROJECT_SUMMARY_MAP = {
    PS_OVERVIEW_TITLE: SupportedPrompts.PROJECT_OVERVIEW_SECTION,
    PS_FEATURE_TITLE: SupportedPrompts.PROJECT_FEATURE_SECTION,
    PS_ENTITIES_TITLE: SupportedPrompts.PROJECT_ENTITIES_SECTION,
    PS_SUBSYSTEM_TITLE: SupportedPrompts.PROJECT_SUBSYSTEM_SECTION,
    PS_DATA_FLOW_TITLE: SupportedPrompts.PROJECT_DATA_FLOW_SECTION
}
