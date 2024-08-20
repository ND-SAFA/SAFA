import random
from typing import Callable, Dict, Iterable, List, Tuple, TypeVar

from gen_common.constants.symbol_constants import UNDERSCORE
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.llm.llm_trainer import LLMTrainer
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.util.enum_util import EnumDict

from gen.health.health_contants import ALL_SELECTION, RANDOM_SELECTION


def expand_query_selection(artifact_df: ArtifactDataFrame, query_ids: List[str]) -> List[str]:
    """
    Expands query ids if a selection command is found.
    :param artifact_df: Artifact dataframe containing project artifacts.
    :param query_ids: List of query ids which may contain selection commands.
    :return: List of artifacts ids in query.
    """
    command = None
    if isinstance(query_ids, list) and len(query_ids) == 1:
        command = query_ids[0]
    elif isinstance(query_ids, str):
        command = query_ids

    if command:
        artifact_ids = list(artifact_df.index)
        command = command.upper()
        if command == ALL_SELECTION:
            query_ids = list(artifact_ids)
        if command == RANDOM_SELECTION:
            query_ids = [random.choice(artifact_ids)]

        if RANDOM_SELECTION in command:
            try:
                k = int(command.split(UNDERSCORE)[-1])
                query_ids = random.sample(artifact_ids, k)
            except Exception as e:
                pass

    return query_ids


PromptGeneratorReturnType = Tuple[PromptBuilder, EnumDict]
PromptGeneratorType = Callable[[Artifact], PromptGeneratorReturnType]

ItemType = TypeVar("ItemType")


def complete_iterable_prompts(items: Iterable[ItemType],
                              prompt_generator: Callable[[Artifact], Tuple[PromptBuilder, EnumDict]],
                              llm_manager: AbstractLLMManager) -> List[Tuple[ItemType, Dict]]:
    prompts: List[EnumDict] = []
    builders: List[PromptBuilder] = []
    for a in items:
        a_builder, a_prompt = prompt_generator(a)
        builders.append(a_builder)
        prompts.append(a_prompt)

    message_prompts = [p[PromptKeys.PROMPT] for p in prompts]
    system_prompts = [p[PromptKeys.SYSTEM] if p.get(PromptKeys.SYSTEM, None) else None for p in prompts]
    output = LLMTrainer.predict_from_prompts(llm_manager=llm_manager,
                                             prompt_builders=builders,
                                             message_prompts=message_prompts,
                                             system_prompts=system_prompts)

    parsed_responses = []
    for artifact, builder, prediction in zip(items, builders, output.predictions):
        if prediction is None:
            logger.info(f"Unable to parse response for artifact: {artifact}")
            continue
        prompt_id = builder.prompts[-1].args.prompt_id
        parsed_artifact_response = prediction[prompt_id]
        parsed_responses.append(parsed_artifact_response)
    return list(zip(items, parsed_responses))
