import os

from paper.pipeline.base import RankingStore, create_artifact_map
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_task import LLMCompletionType


def create_ranking_prompts(s: RankingStore):
    project_path = s.project_path
    project_path = os.path.expanduser(project_path)
    project_reader = StructuredProjectReader(project_path)
    artifact_df, _, _ = project_reader.read_project()

    trace_entries = s.trace_entries
    trace_queries = create_trace_queries(trace_entries)
    artifact_map = create_artifact_map(artifact_df)

    prompts = []
    source_ids = []
    for s_name, target_ids in trace_queries.items():
        target_ids.sort()
        prompt = create_prompts(artifact_map, s_name, target_ids, s.prompt_question, s.prompt_format)
        prompts.append(prompt)
        source_ids.append(s_name)
    s.source_ids = source_ids
    s.prompts = prompts


def create_trace_queries(entries):
    """
    Maps source artifacts to their predicted target artifacts.
    :param entries:
    :return:
    """
    entry_map = {}
    for entry in entries:
        source = entry["source"]
        target = entry["target"]
        if source not in entry_map:
            entry_map[source] = []
        entry_map[source].append(target)
    return entry_map


def create_prompts(artifact_map, source_name, target_names, base_prompt, suffix_prompt):
    def format_artifact(artifact_name: str):
        body = artifact_map[artifact_name]
        body = body.replace("\n\n", "\n")
        return f"ID: {artifact_name}\nBODY: {body}\n\n"

    prompt = base_prompt + f"\"{artifact_map[source_name]}\"\n\n# Artifacts\n\n"
    for t_name in target_names:
        prompt += format_artifact(t_name)
    prompt += f"\n{suffix_prompt}"
    return prompt


def complete_ranking_prompts(s: RankingStore):
    manager = AnthropicManager()
    prompts = s.prompts
    params = {
        "prompt": [f"\n\nHuman: {p}\n\nAssistant:" for p in prompts],
        "max_tokens_to_generate": 400,
        "temperature": 0
    }
    batch_response = manager.make_completion_request(LLMCompletionType.GENERATION, **params)
    s.batch_response = batch_response
