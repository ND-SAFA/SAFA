from collections import defaultdict
from typing import Dict, List, Tuple

from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.objects.trace import Trace
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.llm_util import LLMUtil, PromptGeneratorType

from gen.health.concepts.concept_args import ConceptArgs
from gen.health.concepts.matching.concept_matching_prompts import LLMConceptMatchingPromptFormat, LLM_CONCEPT_MATCHING_SYSTEM_PROMPT
from gen.health.concepts.matching.concept_matching_state import ConceptMatchingState
from gen.health.concepts.matching.types.concept_direct_match import ConceptDirectMatch


class LLMConceptMatchingStep(AbstractPipelineStep):
    """
    Prompts LLM to list (and define) all acronyms found in artifact content.

    * This is just a starting point and more robust entity extraction must be researched.
    """

    def _run(self, args: ConceptArgs, state: ConceptMatchingState) -> None:
        """
        Extracts the most important entities from the target artifact.
        :param args: Contains artifact content to extract entities from.
        :param state: Stored entity df.
        :return: None
        """
        content_map = {a[ArtifactKeys.ID]: a[ArtifactKeys.CONTENT] for a in args.get_concept_artifacts() + args.get_query_artifacts()}
        embeddings_manager = EmbeddingsManager(content_map, create_embeddings_on_init=True)

        artifact2match = LLMConceptMatchingStep._create_artifact2match(state.direct_matches)
        prediction_output = LLMUtil.complete_iterable_prompts(
            items=args.get_query_artifacts(),
            prompt_generator=self._create_prompt_generator(
                args,
                args.llm_manager.prompt_args,
                artifact2match,
                embeddings_manager
            ),
            llm_manager=args.llm_manager
        )

        text2concept = {c[ArtifactKeys.ID].lower(): c[ArtifactKeys.ID] for c in args.get_concept_artifacts()}
        state.predicted_matches = self._parse_responses(prediction_output,
                                                        artifact2match,
                                                        text2concept)

    @staticmethod
    def _create_prompt_generator(args: ConceptArgs,
                                 llm_args: LLMPromptBuildArgs,
                                 artifact2previous_matches: Dict[str, List[str]],
                                 embeddings_manager: EmbeddingsManager
                                 ) -> PromptGeneratorType:
        """
        Create prompt generator for concept prediction for a given query artifact.
        :param args: Concept args containing artifacts.
        :param llm_args: LLM args establishing which provider and model to use.
        :param artifact2previous_matches: List of previous matches for each artifact.
        :param embeddings_manager: Embedding manager used to search for related concepts with.
        :return: PromptGenerator .
        """

        def generator(artifact: Artifact):
            """
            Generates prompt concept matching prompt for artifact.
            :param artifact: The artifact to create trace predictions to concepts.
            :return: Builder and prompt.
            """
            builder = PromptBuilder(
                prompts=[
                    MultiArtifactPrompt("Project Concepts and Terminology", build_method=MultiArtifactPrompt.BuildMethod.XML),
                    ArtifactPrompt("# Target Artifact\n"),
                    Prompt(
                        response_manager=JSONResponseManager.from_langgraph_model(
                            LLMConceptMatchingPromptFormat
                        ))
                ],
            )

            query_existing_concepts = artifact2previous_matches[artifact[ArtifactKeys.ID]]
            query_concepts = [c for c in args.get_concept_artifacts() if c[ArtifactKeys.ID] not in query_existing_concepts]
            query_concepts = LLMConceptMatchingStep._get_similar_concepts(embeddings_manager,
                                                                          artifact,
                                                                          query_concepts,
                                                                          args.n_concepts_in_prompt)
            prompt = builder.build(llm_args, artifacts=query_concepts, artifact=artifact)
            prompt[PromptKeys.SYSTEM] = LLM_CONCEPT_MATCHING_SYSTEM_PROMPT
            return builder, prompt

        return generator

    @staticmethod
    def _parse_responses(
            predictions: List[Tuple[Artifact, Dict]],
            artifact2previous_matches: Dict[str, List[str]],
            concept_map: Dict[str, str]
    ) -> List[Trace]:
        """
        Parses model output into trace predictions.
        :param predictions: The parsed predictions for the artifacts.
        :param artifact2previous_matches: List of previous concept matches per artifact.
        :param concept_map: Map of lower case concept id to concept name.
        :return: List of trace links for predicted concepts in artifacts.
        """
        traces = []

        for artifact, builder_output in predictions:
            if builder_output is None:
                logger.info(f"Unable to parse response for artifact: {artifact}")
                continue
            previous_matches = artifact2previous_matches[artifact[ArtifactKeys.ID]]
            for prediction_dict in builder_output["predictions"]:
                predicted_concept_id = prediction_dict["artifact_id"][0]
                predicted_explanation = prediction_dict["explanation"][0]

                predicted_concept_key = predicted_concept_id.lower()
                if predicted_concept_key not in concept_map:
                    print(f"{predicted_concept_key} was predicted but not in concepts...")
                    continue
                concept_id = concept_map[predicted_concept_key]
                if predicted_concept_id not in previous_matches:
                    trace = Trace(
                        source=artifact[ArtifactKeys.ID],
                        target=concept_id,
                        score=1,
                        explanation=f"{predicted_explanation}"
                    )
                    traces.append(trace)
        return traces

    @staticmethod
    def _get_similar_concepts(
            embeddings_manager: EmbeddingsManager,
            query_artifact: Artifact,
            concept_artifacts: List[Artifact],
            n_top: int
    ) -> List[Artifact]:
        """
        Finds the n most semantically similar concepts to each query artifact.
        :param embeddings_manager: Embedding manager used to compare artifacts.
        :param query_artifact: The artifact whose similar concepts are retrieved.
        :param concept_artifacts: List of concepts to select from.
        :param n_top: Number of concepts to return.
        :return: Concepts selected.
        """
        query_id = query_artifact[ArtifactKeys.ID]
        concept_ids = [c[ArtifactKeys.ID] for c in concept_artifacts]
        similarity_matrix = embeddings_manager.compare_artifacts([query_id], concept_ids)
        sorted_concepts = sorted(zip(concept_artifacts, similarity_matrix[0]), key=lambda x: x[1], reverse=True)
        selected_concepts = [concept for concept, score in sorted_concepts[:n_top]]
        return selected_concepts

    @staticmethod
    def _create_artifact2match(matches: List[ConceptDirectMatch]):
        """
        Creates map of matches to each artifact.
        :param matches: List of matches.
        :return: Map of artifact to its matches.
        """
        artifact2match = defaultdict(list)
        for m in matches:
            artifact2match[m["artifact_id"]].append(m["concept_id"])
        return artifact2match
