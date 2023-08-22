from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager

CODE_SUMMARY = [Prompt("\n\n# Task\n"
                       "1. Provide a list of answers about the following questions about the code:"
                       "\n- What are the inputs/outputs of this code?"
                       "\n- What is the code doing?"
                       "\nUse `# Project Specification` to guide your context of the system. Enclose your answer in <notes></notes>"
                       "\n\n2. Write a polished summary of the code in one cohesive, detailed. paragraph."
                       "Write in an active voice and assume your audience is familiar with software system this code belongs to."
                       "\n\n",
                       PromptResponseManager(response_tag="summary")),
                ArtifactPrompt(include_id=False, prompt_start="# Code\n")]

NL_SUMMARY = [
    Prompt("Summarize the following, focusing on the high-level usage.\n", PromptResponseManager(response_tag="summary")),
    ArtifactPrompt(include_id=False)]

CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                  "You are given some code from the system and asked to summarize it.\n")
