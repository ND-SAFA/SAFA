from enum import Enum

from common_resources.data.summarizer.artifact_summary_prompts import CODE_SUMMARY, NL_SUMMARY


class ArtifactSummaryTypes(Enum):
    CODE_BASE = CODE_SUMMARY
    NL_BASE = NL_SUMMARY
