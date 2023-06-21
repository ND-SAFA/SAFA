from typing import Callable, Dict, List

from paper.common.completion_util import complete_prompts
from paper.common.prompt_builder import PromptBuilder
from paper.pipeline.map_step import process_ranked_artifacts

GenericSorter = Callable[[List[str], List[str], Dict], List[str]]  # source names, target names, artifact map -> sorted target names


def test_sorter(source_names, target_names, artifact_map) -> List[str]:
    target_names.sort()
    return target_names


DEFAULT_SORTING_PROMPT = "Below is a set of software artifacts. Identify the general functionality of the system and " \
                         "sort the artifacts from most to least important to the system functionality. " \
                         "Provide the ranked list of comma delimited artifact ids."


def claude_sorter(source_names, target_names, artifact_map) -> Dict[str, List[str]]:
    builder = PromptBuilder()
    builder.with_task(DEFAULT_SORTING_PROMPT)
    for t_name in target_names:
        builder.with_artifact(t_name, artifact_map[t_name])
    prompt = builder.get()
    model = "claude-v1.3-100k"  # "claude-v1.3-100k", "claude-instant-v1-100k"
    batch_response = complete_prompts([prompt], model=model, max_tokens=600)
    batch_ranked_target_artifacts = process_ranked_artifacts(batch_response, target_names)
    sorted_target_artifacts = batch_ranked_target_artifacts[0]

    source2target = {}

    for s in source_names:
        source2target[s] = sorted_target_artifacts
    return source2target


registered_sorters: Dict[str, GenericSorter] = {
    "test": test_sorter,
    "claude": claude_sorter
}
