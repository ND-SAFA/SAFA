from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt

CODE_SECTION_ID = "# Code to Summarize"
CODE_SECTION_HEADER = f"\n\n\n{CODE_SECTION_ID}\n"
CODE_SUMMARY = [Prompt("\n\n# Task\n"
                       "First, provide a list of answers about the following questions about the code in the section "
                       f"`{CODE_SECTION_ID}`:\n"
                       "\n- What are the inputs/outputs of this code?"
                       "\n- What is the code achieving?"
                       "\n Enclose your answer in <notes></notes>."
                       f"\n\nThen, write a polished summary in one cohesive, detailed paragraph. "
                       "Write in an active voice and assume your audience is familiar with software system this code belongs to. "
                       "There should be NO specific class or function names, but otherwise include key details about the code."
                       "\n\n",
                       PromptResponseManager(response_tag="summary")),
                ArtifactPrompt(include_id=False, prompt_start=CODE_SECTION_HEADER)]

NL_SUMMARY = [
    Prompt("# Task\n"
           "1. Provide a list of answers to the following questions about the software artifact:"
           "\n- What functionality is described by the artifact?"
           "\n- What are the keywords that capture the functionality of the artifact?"
           "\nEnclose your answer in <notes></notes>"
           "\n\n2. Then, write a short title describing the artifact's functionality followed by its important keywords. "
           "Follow the format TITLE - KEYWORDS. "
           "Write in an active voice and assume your audience is familiar with software system this artifact belongs to."
           "\n\n",
           PromptResponseManager(response_tag="descrip")),
    ArtifactPrompt(include_id=False, prompt_start="\n", build_method=ArtifactPrompt.BuildMethod.XML)]

CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = QuestionPrompt("Use the information below to understand the project.")
NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                "You are given a software artifact from the system and asked to describe it.\n")
