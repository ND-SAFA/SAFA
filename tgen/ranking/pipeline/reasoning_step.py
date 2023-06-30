from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.ranking.pipeline.base import RankingStore
from tgen.ranking.pipeline.ipipeline import iPipeline

from tgen.util.list_util import ListUtil

MAX_ARTIFACTS_PER_PROMPT = 60


class ReasoningStep(iPipeline):
    def __init__(self):
        steps = [ReasoningStep.create_reasoning_prompt,
                 ReasoningStep.complete_reasoning_prompts,
                 ReasoningStep.process_reasoning_prompts]
        super().__init__(steps)

    @staticmethod
    def create_reasoning_prompt(s: RankingStore):
        artifact_map = s.artifact_map
        source_names = s.source_ids

        prompts = []
        for s_name in source_names:
            s_prompts = ReasoningStep.create_batched_reasoning_prompts(artifact_map, s_name, s)
            start = len(prompts)
            end = start + len(s_prompts)
            for i in range(start, end):
                s.reasoning_prompts2source[i] = s_name
            prompts.extend(s_prompts)

        s.reasoning_prompts = prompts

    @staticmethod
    def complete_reasoning_prompts(s: RankingStore):
        reasoning_responses = complete_prompts(s.reasoning_prompts, max_tokens=4000)
        s.reasoning_responses = reasoning_responses

    @staticmethod
    def process_reasoning_prompts(s: RankingStore):
        responses = s.reasoning_responses
        source2reasons = {s: "" for s in s.source_ids}
        for prompt_index, prompt_response in enumerate(responses.batch_responses):
            source_name = s.reasoning_prompts2source[prompt_index]
            source2reasons[source_name] += prompt_response + "\n"
        source2reasons = {s: c.strip() for s, c in source2reasons.items()}
        s.source2reason = source2reasons

    @staticmethod
    def remove_tag(body: str, tag: str):
        open_tag = f"<{tag}>"
        start = body.index(open_tag)
        if start == -1 or start >= len(body):
            return body
        return body[start:]

    @staticmethod
    def create_batched_reasoning_prompts(artifact_map, source_name, s: RankingStore):
        source_body = artifact_map[source_name]
        target_names = s.source2targets[source_name]
        batches = ListUtil.batch(target_names, MAX_ARTIFACTS_PER_PROMPT)
        prompts = []
        target_index = 0
        for target_names in batches:
            prompt_builder = RankingPromptBuilder(goal=s.reasoning_goal,
                                                  instructions=s.reasoning_instructions,
                                                  query=source_body,
                                                  body_title="# Artifacts")
            for target_artifact_name in target_names:
                prompt_builder.with_artifact(target_index, artifact_map[target_artifact_name])
                target_index += 1
            prompt = prompt_builder.get()
            prompts.append(prompt)
        return prompts

    def __call__(self, store):
        for step in self.steps:
            step(store)
