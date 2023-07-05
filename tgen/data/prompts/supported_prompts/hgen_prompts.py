from token import COMMA

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager

INSTRUCTION_CREATION_PROMPT = Prompt("Break the process of reverse engineering {target_type} from {source_type} into steps. "
                                     "The steps should be generalized so that they would work on any software project. "
                                     "Each step should include instructions on how to perform the step,"
                                     " a description of the expected deliverable, and a one word unique name for the step. "
                                     "The deliverable descriptions should indicate the type of information "
                                     "that would satisfy the step, rather than providing a specific example. "
                                     "The final step should be the {target_type} creation. ",
                                     PromptResponseManager(response_tag={"step":
                                                                             ["name",
                                                                              "instructions",
                                                                              "expected-deliverable-description"]},
                                                           id2tag={"step": "step", "instructions": "instructions",
                                                                   "deliverable": "expected-deliverable-description",
                                                                   "name": "name"},
                                                           response_instructions_format="Each step should be enclosed in {step} "
                                                                                        "with the instructions enclosed "
                                                                                        "in {instructions}, "
                                                                                        "a general description "
                                                                                        "of the expected deliverable "
                                                                                        "from the step enclosed in {deliverable},"
                                                                                        "and the step name enclosed in {name}."))
RELATED_ARTIFACT_PROMPT = Prompt("You are given {target_type} and a list of numbered {source_type} that may be related. "
                                 "Select the {source_type} that would be traced to the {target_type} "
                                 "and output the numbers associated with the linked {source_type} in a comma deliminated list.",
                                 response_manager=PromptResponseManager(response_tag="related-numbers",
                                                                        formatter=lambda _, val: [int(v) for v in val.split(COMMA)]))
GENERATION_PROMPT = Prompt("You are an engineering working on a software system and your goal is to reverse engineer "
                           "{source_type}s from {target_type}s. You are given a numbered list of descriptions of the "
                           "{source_type}s in the system and you must complete each step below with the "
                           "end goal of producing the {target_type}s.")
