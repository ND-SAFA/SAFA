from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager

CODE_SUMMARY = [Prompt("Provide a few sentences describing the high-level usage of the code below. "
                       "Do not focus on implementation details and assume your audience works on this system",
                       PromptResponseManager(response_tag="summary")), ArtifactPrompt(include_id=False)]

NL_SUMMARY = [
    Prompt("Summarize the following, focusing on the high-level usage.\n", PromptResponseManager(response_tag="summary")),
    ArtifactPrompt(include_id=False)]
