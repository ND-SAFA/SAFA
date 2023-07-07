from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.util.supported_enum import SupportedEnum


class SupportedPromptsOld(SupportedEnum):
    """
    Enumerates supported prompts used for completion tasks.
    """
    
    UAV_SYSTEM_REQUIREMENT = [Prompt("Given a summary of python code, write a system-level requirement\n "
                                     "The requirements should reference physical world entities related to the UAV systems, "
                                     "be numbered system level requirements and use the 'shall' format:"),
                              ArtifactPrompt(include_id=False)]
    FUNCTIONALITIES = [Prompt("I am giving you a numbered list of artifact descriptions for a software system. "
                              "Describe the functionalities of the system that would be "
                              "important for grouping related artifacts belonging to a single {target_artifact_type}. "
                              "Focus on aspects that are unique to this system but remain high-level.",
                              PromptResponseManager(response_tag="feature")),
                       MultiArtifactPrompt(include_ids=False)]
    RE_CLUSTER_FEATURE = [Prompt("I am giving you a numbered list of software artifact descriptions relating to {feature}. "
                                 "Determine sub features that would divide the artifacts into groups "
                                 "belonging to a single {target_artifact_type}. "
                                 "Here are some existing features that may be used for grouping the artifacts. {features}"
                                 "Focus on aspects that are unique to this system but remain high-level. "
                                 "Group the artifacts by these sub features "
                                 "where each group has at least 2 artifacts and no more than 10 artifacts. "
                                 "Artifacts should belong to at least 1 group. ",
                                 PromptResponseManager(response_tag={"group": ["feature", "artifact"]},
                                                       response_instructions_format="Enclose your answer in {}")),
                          MultiArtifactPrompt(include_ids=False)]
    CLUSTER_FROM_FEATURES = [Prompt("I am giving you a list of features for creating {target_artifact_type}s "
                                    "and a numbered list of software artifact descriptions. "
                                    "Group all artifacts with the features that relate to it. "
                                    "If none of the features relate to the description, "
                                    "create a new feature for a {target_artifact_type} "
                                    "which relates to other artifacts as well "
                                    "and group these related artifacts with it. "
                                    "If the feature is too broad, you may replace it with sub features. "
                                    "Groups must contain at least 2 artifacts and at most 10 artifacts "
                                    "and all artifacts should belong to at least one group.  "
                                    "Focus on aspects that are unique to this system but remain high-level. ",
                                    PromptResponseManager(response_tag="group")),
                             MultiArtifactPrompt(include_ids=False)]
    ARTIFACT_EXAMPLE = [Prompt("Write a single example of a {artifact_type} body.", PromptResponseManager(response_tag="example"))]
