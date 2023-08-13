from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager

CODE_SUMMARY = [Prompt("\n\n# Task\nProvide a paragraph summarizing the functionality of the code. "
                       "Include what what system behavior it helps support, how it does so, and why it exists in the system. "
                       "Assume you are writing to a novice developer.",
                       PromptResponseManager(response_tag="summary")),
                ArtifactPrompt(include_id=False)]

NL_SUMMARY = [
    Prompt("Summarize the following, focusing on the high-level usage.\n", PromptResponseManager(response_tag="summary")),
    ArtifactPrompt(include_id=False)]

CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                  "You are given some code from the system and asked to summarize it.\n")
