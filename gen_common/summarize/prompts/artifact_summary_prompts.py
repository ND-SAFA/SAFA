from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager

CODE_SECTION_ID = "# Code to Summarize"
CODE_SECTION_HEADER = f"{CODE_SECTION_ID}\n"
CODE_SUMMARY = [ArtifactPrompt(include_id=False, prompt_start=CODE_SECTION_HEADER),
                Prompt("\n\n# Task\n"
                       "First, answer this question with as much detail and accuracy as possible."
                       "\n- What can a user achieve through this code?"
                       "\n Do NOT reference specific class or function names, but instead describe them in detail. "
                       "\n Your answer should be in the form of a long, detailed paragraph. Do not speculate or make up information, "
                       "use only information directly from the code. "
                       "Enclose your answer in <draft></draft>."
                       f"\n\nThen, create a cohesive, detailed paragraph, encapsulating all the details from your draft. "
                       "Focus on describing the behavior provided to the user "
                       "while interweaving the details of how it provides such behavior."
                       "Write in an active voice and assume your audience is familiar with software system this code belongs to. "
                       "Do not make conclusions about the code and only provide information.",
                       response_manager=XMLResponseManager(response_tag="summary"))
                ]

CODE_SUMMARY_AS_NL = [ArtifactPrompt(include_id=False, prompt_start=CODE_SECTION_HEADER),
                      Prompt("\n\n# Task\n"
                             "First, answer this question with as much detail and accuracy as possible."
                             "\n- What can a user achieve through this code?"
                             "\n Do NOT reference specific class or function names, but instead describe them in detail. "
                             "\n Your answer should be in the form of a long, "
                             "detailed paragraph. Do not speculate or make up information, "
                             "use only information directly from the code. "
                             "Enclose your answer in <notes></notes>."
                             "\n\nThen, using your notes, create a {target_type} artifact for this code that describes the behavior "
                             "provided to the user. You should use the following format when creating the {target_type}\n"
                             "{format} ",
                             response_manager=XMLResponseManager(response_tag="summary"))
                      ]

NL_SUMMARY = [
    Prompt(f"Condense the information in the artifact below into free form text that captures only the key entities and actions. "
           f"For example, 'The system shall provide a secure login and authentication mechanism "
           f"for users to access their accounts.' could be condensed to "
           f"'secure login and authentication for user accounts'. ",
           response_manager=XMLResponseManager(response_tag="descrip")),
    ArtifactPrompt(include_id=False, prompt_start="\n", build_method=ArtifactPrompt.BuildMethod.XML)]

CODE_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = QuestionPrompt("Use the information below to understand the project.")
NL_SUMMARY_WITH_PROJECT_SUMMARY_PREFIX = Prompt("# Goal\nBelow is a description of software project. "
                                                "You are given a software artifact from the system and asked to describe it.\n")
