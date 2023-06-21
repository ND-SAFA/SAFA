from typing import Callable, Dict, List

from paper.common.completion_util import complete_prompts
from paper.common.prompt_builder import PromptBuilder

GenericSorter = Callable[[List[str], List[str], Dict], List[str]]  # source names, target names, artifact map -> sorted target names


def test_sorter(source_names, target_names, artifact_map) -> List[str]:
    target_names.sort()
    return target_names


DEFAULT_SORTING_PROMPT = "Rank the following artifacts from most to least " \
                         "important to the overall system functionality. " \
                         "Provide the ranked artifacts as comma delimited list of artifact ids."


def claude_sorter(source_names, target_names, artifact_map) -> List[str]:
    builder = PromptBuilder()
    builder.with_task(DEFAULT_SORTING_PROMPT)
    for t_name in target_names:
        builder.with_artifact(t_name, artifact_map[t_name])
    prompt = builder.get()
    batch_response = complete_prompts([prompt])


registered_sorters: Dict[str, GenericSorter] = {
    "test": test_sorter,
    "claude": claude_sorter
}
