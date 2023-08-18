from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager

CODE_SUMMARY = [Prompt("\n\n# Task\n"
                       "Provide a detailed summarization of the code while answering the following questions:"
                       "- What is the main functionality this code provides?"
                       "- Why is this functionality important?"
                       "- What is the purpose of this functionality in the context of a software system?"
                       "Write the summary in an active voice. "
                       "Assume your audience is familiar with software system this code belongs to.",
                       PromptResponseManager(response_tag="summary")),
                ArtifactPrompt(include_id=False)]

NL_SUMMARY = [
    Prompt("Summarize the following, focusing on the high-level usage.\n", PromptResponseManager(response_tag="summary")),
    ArtifactPrompt(include_id=False)]

CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                  "You are given some code from the system and asked to summarize it.\n")
