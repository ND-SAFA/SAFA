from dataclasses import dataclass

from gen_common.infra.base_object import BaseObject


@dataclass
class PromptConfig(BaseObject):
    """
    :param requires_trace_per_prompt: True if a trace link is required for each prompt
    """
    requires_trace_per_prompt: bool
    """
    :param requires_artifact_per_prompt: True if an artifact is required for each prompt 
    """
    requires_artifact_per_prompt: bool
    """
    :param requires_all_artifacts: True if all artifacts are required for each prompt 
    """
    requires_all_artifacts: bool
