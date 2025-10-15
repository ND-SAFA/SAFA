from typing import Dict, List, Tuple

from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.util.llm_util import LLMUtil, PromptGeneratorReturnType, PromptGeneratorType

from gen.health.concepts.extraction.concept_extraction_prompt import UNDEFINED_ENTITY_EXTRACTION_PROMPT, \
    UndefinedEntityExtractionPromptFormat
from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.matching.steps.direct_concept_matching_step import DirectConceptMatchingStep
from gen.health.concepts.matching.types.concept_variants import ConceptVariants
from gen.health.health_args import HealthArgs

USED_CONCEPTS_TITLE = "# Concepts Used In Artifact"


class ExtractUndefinedConceptsStep(AbstractPipelineStep):
    def _run(self, args: HealthArgs, state: ConceptExtractionState) -> None:
        """
        Extracts undefined concepts in query artifacts.
        :param args: Concept args containing dataset and query artifacts.
        :param state: State used to store identified undefined concepts.
        :return: None
        """
        predictions = LLMUtil.complete_iterable_prompts(
            items=args.get_query_artifacts(),
            prompt_generator=self._create_prompt_generator(
                args.llm_manager.prompt_args,
                args.get_concept_artifacts(),
                args.dataset.trace_dataset.trace_df
            ),
            llm_manager=args.llm_manager
        )
        artifact2undefined = self._parse_predictions(predictions)
        state.artifact2undefined = self._filter_defined_concepts(artifact2undefined, args.get_concept_artifacts())

    @staticmethod
    def _create_prompt_generator(llm_format_args: LLMPromptBuildArgs,
                                 concept_artifacts: List[Artifact],
                                 trace_df: TraceDataFrame) -> PromptGeneratorType:
        """
        Creates prompt generator for extracting undefined concepts in query artifacts.
        :param llm_format_args: The LLM provider format arguments.
        :param concept_artifacts: List of artifacts representing concepts in project.
        :param trace_df: Trace data frame containing project trace links.
        :return: Prompt generator.
        """

        def prompt_generator(artifact: Artifact) -> PromptGeneratorReturnType:
            """
            Generates undefined concept extraction prompt for artifact.
            :param artifact: The artifact to generate prompt for.
            :return: Prompt builder and built prompt.
            """
            concept_map = {a[ArtifactKeys.ID]: a for a in concept_artifacts}
            linked_concepts: List[Artifact] = ExtractUndefinedConceptsStep._get_connected_concepts(artifact, concept_map, trace_df)
            prompts = [
                MultiArtifactPrompt(USED_CONCEPTS_TITLE) if linked_concepts else Prompt(
                    f"{USED_CONCEPTS_TITLE}\nNo concepts defined."),
                ArtifactPrompt("# Target Artifact"),
                Prompt(
                    response_manager=JSONResponseManager.from_langgraph_model(
                        UndefinedEntityExtractionPromptFormat
                    ))
            ]

            builder = PromptBuilder(prompts=prompts)
            prompt = builder.build(llm_format_args, artifact=artifact, artifacts=linked_concepts)
            prompt[PromptKeys.SYSTEM] = UNDEFINED_ENTITY_EXTRACTION_PROMPT
            return builder, prompt

        return prompt_generator

    @staticmethod
    def _parse_predictions(predictions: List[Tuple[Artifact, Dict]]) -> Dict[str, List[str]]:
        """
        Parses predictions for undefined concepts in artifacts.
        :param predictions: LLM predictions for undefined concepts in query artifacts.
        :return: Map of artifact ids to list of undefined concepts.
        """
        artifact2undefined_concepts = {}
        for artifact, prediction in predictions:
            artifact2undefined_concepts[artifact[ArtifactKeys.ID]] = prediction["undefined_concepts"]
        return artifact2undefined_concepts

    @staticmethod
    def _filter_defined_concepts(artifact2undefined_concepts: Dict[str, List[str]],
                                 concept_artifacts: List[Artifact]) -> Dict[str, List[str]]:
        """
        Removes any undefined concepts that are already defined in concept artifacts.
        :param artifact2undefined_concepts: Map of artifact ids to undefiend concepts.
        :param concept_artifacts: List of concept artifacts already in project.
        :return: Artifact2undefined concept but containing only unique entries.
        """
        concept_variants = [ConceptVariants(a[ArtifactKeys.ID]) for a in concept_artifacts]
        filtered_dict = {}
        for a, undefined_concepts in artifact2undefined_concepts.items():
            filtered_dict[a] = ExtractUndefinedConceptsStep.get_unique_concepts(undefined_concepts, concept_variants)
        return filtered_dict

    @staticmethod
    def _get_connected_concepts(artifact: Artifact, concept_map: Dict[str, Artifact], trace_df: TraceDataFrame) -> List[Artifact]:
        """
        Returns concept artifacts connected to artifact.
        :param artifact: Artifact whose concepts are returned.
        :param concept_map: Map of id to artifact for concepts.
        :param trace_df: Trace data frame containing links to artifact and concepts.
        :return: List of concept ids connected to artifact.
        """
        concept_ids = set(concept_map.keys())
        artifact_traces = trace_df.filter_for_parents_or_children(artifact[ArtifactKeys.ID])
        connected_concepts: List[Artifact] = []
        for t in artifact_traces:
            for t_key in [TraceKeys.SOURCE, TraceKeys.TARGET]:
                if t_key in concept_ids:
                    concept = concept_map[t[t_key]]
                    connected_concepts.append(concept)
        return connected_concepts

    @staticmethod
    def get_unique_concepts(concepts: List[str], concept_variants: List[ConceptVariants]):
        """
        Returns unique concepts not already defined in concept variants.
        :param concepts: List of concepts to filter out if not unique.
        :param concept_variants: List of concepts variants checked against each concept.
        :return: List of unique concepts.
        """
        unique = []
        for undefined_concept in concepts:
            if not ExtractUndefinedConceptsStep._is_unique(undefined_concept, concept_variants):
                continue
            unique.append(undefined_concept)
        return unique

    @staticmethod
    def _is_unique(concept_id: str, concept_variants: List[ConceptVariants]) -> bool:
        """
        Checks whether given concept id is contained in concept_variants.
        :param concept_id: The concept id to check for uniqueness.
        :param concept_variants: The variants available to check against.
        :return: Whether concept id is contained in concept_variants.
        """
        for cv in concept_variants:
            start_loc, end_loc = DirectConceptMatchingStep.find_concept_usages(concept_id, cv)
            if start_loc is not None:
                return False
        return True
