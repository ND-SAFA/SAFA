from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager

CODE_SUMMARY = [Prompt("\n\n# Task\n"
                       "1. Provide a list of answers about the following questions about the code:"
                       "\n- What are the inputs/outputs of this code?"
                       "\n- What is the code doing?"
                       "\nUse `# Project Specification` to guide your context of the system. Enclose your answer in <notes></notes>"
                       "\n\n2. Write a polished summary of the code in one cohesive, detailed paragraph."
                       "Write in an active voice and assume your audience is familiar with software system this code belongs to."
                       "\n\n",
                       PromptResponseManager(response_tag="summary")),
                ArtifactPrompt(include_id=False, prompt_start="# Code\n")]

NL_SUMMARY = [
    Prompt("# Task\n"
           "1. Provide a list of answers to the following questions about the software artifact:"
           "\n- What is the functionality described by the artifact?"
           "\n- What part of the system does the artifact affect? "
           "\n- Why is this artifact important to the overall system? "
           "\nEnclose your answer in <notes></notes>"
           "\n\n2. Write a polished summary of the software artifacts in one cohesive, detailed paragraph. "
           "Elaborate on the meaning of any acronyms or system terminology. "
           "Write in an active voice and assume your audience is familiar with software system this artifact belongs to."
           "\n\n",
           PromptResponseManager(response_tag="summary")),
    ArtifactPrompt(include_id=False, prompt_start="\n", build_method=ArtifactPrompt.BuildMethod.XML)]

CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                  "You are given some code from the system and asked to summarize it.\n\n\n")
NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                "You are given a software artifact from the system and asked to summarize it.\n")
