from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt

CHUNK_PROMPT = QuestionnairePrompt(
    instructions="Your goal is to break the following software artifact into chunks while retaining the key information. "
                 "To accomplish this, go through each sentence and follow each of these steps: ",
    question_prompts=[Prompt("First, identify whether the sentence conveys important information about the artifact. "
                             "If it does, continue to the next step. Otherwise, proceed to the next sentence. "),
                      Prompt("Then, de-contextualize the sentence - make sure that the sentence makes sense by itself by "
                             "replacing pronouns with specific nouns. "),
                      Prompt(response_manager=PromptResponseManager(response_tag="chunk",
                                                                    response_instructions_format="Output the de-contextualized "
                                                                                                 "sentence enclosed in {}")),
                      Prompt("Continue to the next sentence and repeat process. ")
                      ])
