import json
from collections import defaultdict
from typing import Dict, List

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.util.list_util import ListUtil
from gen_common.util.llm_util import LLMUtil

from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.health_args import HealthArgs

_HEADER = "# Project Terms"
_SYSTEM_PROMPT = (
    f"You are given a list of terms extracts from artifacts of a project (`{_HEADER}`). "
    "Your job is group terms that are referencing the same concepts in the project. "
    "Create a dictionary mapping the unique term to list of alias terms present in the prompt "
)
_FORMAT_JSON = json.dumps({"base_term_1": ["project_term_1", "project_term_2"]})
_FORMAT = f"Please format your response like so:\n{_FORMAT_JSON}"


class CondenseUndefinedConceptsStep(AbstractPipelineStep[HealthArgs, ConceptExtractionState]):
    def _run(self, args: HealthArgs, state: ConceptExtractionState) -> None:
        """
        Condenses current undefined concepts into unique set using LLM.
        :param args: Health args containing artifacts and configuration details.
        :param state: State used to store condensed undefined entities.
        :return: None. Undefined entities are modified in place.
        """
        undefined2artifacts = self.create_undefined2artifacts(state.artifact2undefined)
        if len(undefined2artifacts) == 0:
            state.undefined_concepts = []
        elif len(undefined2artifacts) == 1:
            logger.info(f"Skipping concept condensation step because only single concept exists.")
            undefined_concept = list(undefined2artifacts.keys())[0]
            state.undefined_concepts = [
                UndefinedConcept(
                    concept_id=undefined_concept,
                    artifact_ids=undefined2artifacts[undefined_concept],
                    definition=EMPTY_STRING
                )
            ]
        else:
            state.undefined_concepts = self.generate_condensed_concepts(undefined2artifacts,
                                                                        args.llm_manager,
                                                                        args.n_concepts_in_prompt)

    @staticmethod
    def generate_condensed_concepts(undefined2artifacts: Dict[str, List[str]],
                                    llm_manager: AbstractLLMManager,
                                    n_concepts: int) -> List[UndefinedConcept]:
        """
        Prompts LLM to condense overlapping concepts.
        :param undefined2artifacts: Map of undefined concepts to artifacts referencing them.
        :param llm_manager: The LLM manager to use.
        :param n_concepts: The maximum number of concepts to show to the model.
        :return: List of undefined, but condensed concepts.
        """
        assert len(undefined2artifacts) > 1, "Expected at least two undefined concepts."
        concept_ids = sorted(undefined2artifacts.keys())  # TODO: Replace with clustering to improve robustness
        batches = ListUtil.batch(concept_ids, n=n_concepts)

        def generator(batch: List[str]):
            """
            Creates prompt builder and prompt for given batch of concepts.
            :param batch: The batch of concepts to include in each prompt.
            :return: Builder and prompt.
            """
            concept_content = NEW_LINE.join([f"- {b}" for b in batch])
            prompt_content = f"{_HEADER}\n{concept_content}"
            prompt = Prompt(
                prompt_content,
                response_manager=JSONResponseManager(
                    parse_all=True,
                    response_instructions_format=_FORMAT
                )
            )
            builder = PromptBuilder(prompts=[prompt])
            prompt = builder.build(llm_manager.prompt_args)
            prompt[PromptKeys.SYSTEM] = _SYSTEM_PROMPT
            return builder, prompt

        llm_output = LLMUtil.complete_iterable_prompts(batches, generator, llm_manager)
        predictions: List[Dict] = [batch_prediction for batch, batch_prediction in llm_output]

        undefined_concepts = CondenseUndefinedConceptsStep._parse_undefined_concept_response(predictions, undefined2artifacts)
        return undefined_concepts

    @staticmethod
    def _parse_undefined_concept_response(output: List[Dict], undefined2artifacts: Dict[str, List[str]]):
        """
        Parses the responses for condensing concepts.
        :param output: Parsed model predictions per batch.
        :param undefined2artifacts: Map of undefined concepts to artifact's referencing them.
        :return: List of undefined concepts aggregated or extracted from artifacts.
        """
        new_concepts = {}
        undefined_concept_ids = set(undefined2artifacts.keys())
        flattened_predictions = [(base_term, associated_concepts)
                                 for batch_output in output
                                 for base_term, associated_concepts in batch_output.items()]

        # Add missing concepts
        referenced_concepts = [r for _, referenced_concepts in flattened_predictions for r in referenced_concepts]
        unreferenced_concepts = set(undefined_concept_ids).difference(set(referenced_concepts))
        for unreferenced_concept in unreferenced_concepts:
            new_concepts[unreferenced_concept] = UndefinedConcept(
                concept_id=unreferenced_concept,
                artifact_ids=undefined2artifacts[unreferenced_concept],
                definition=EMPTY_STRING
            )

        # Process predictions, merge conflicting concepts that may exist between batches
        for term, term_concepts in flattened_predictions:
            term_concepts_artifact_ids = [a for c in term_concepts if c in undefined2artifacts for a in undefined2artifacts[c]]
            if term in new_concepts:
                existing_concept = new_concepts[term]
                existing_concept.artifact_ids = list(set(existing_concept.artifact_ids + term_concepts_artifact_ids))
            else:
                uc = UndefinedConcept(
                    artifact_ids=term_concepts_artifact_ids,
                    concept_id=term,
                    definition=EMPTY_STRING
                )
                new_concepts[term] = uc
        undefined_concepts = list(new_concepts.values())
        return undefined_concepts

    @staticmethod
    def create_undefined2artifacts(artifact2undefined: Dict[str, List[str]]):
        """
        Reverses mapping of artifact to undefined concepts to undefined concepts to related artifacts.
        :param artifact2undefined: Map of artifacts to undefined concepts within each.
        :return: Map of undefined concepts to artifacts referencing them.
        """
        undefined2artifact = defaultdict(list)
        for a_id, undefined in artifact2undefined.items():
            for u_id in undefined:
                undefined2artifact[u_id].append(a_id)
        return undefined2artifact
