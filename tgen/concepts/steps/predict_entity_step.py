from collections import defaultdict
from typing import Dict, List, Tuple

from common_resources.data.keys.prompt_keys import PromptKeys
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.objects.artifact import Artifact
from common_resources.data.objects.trace import Trace
from common_resources.llm.prompts.artifact_prompt import ArtifactPrompt
from common_resources.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from common_resources.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.llm.response_managers.json_response_manager import JSONResponseManager
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from pydantic.v1 import BaseModel, Field

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.concept_match import ConceptMatch
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep

# TODO : I don't like needing to pass around the triplet of (prompt, builder, artifact)

system_prompt = (
    "You are working on a project containing a list of project-specific concepts and terminology "
    "alongside a specific target artifact from the project. "
    "Your job is to predict which concepts are cited in the artifact. "
    "Each artifact has an ID and some content, predict only the IDs contained within the target artifact. "
)


class ExpectedResponse(BaseModel):
    """
    Response for making predictions for cited concepts in target artifact.
    """
    predictions: List[str] = Field(description="List of ID referenced in target artifact.")


class PredictEntityStep(AbstractPipelineStep):
    """
    Prompts LLM to list (and define) all acronyms found in artifact content.

    * This is just a starting point and more robust entity extraction must be researched.
    """

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Extracts the most important entities from the target artifact.
        :param args: Contains artifact content to extract entities from.
        :param state: Stored entity df.
        :return: None
        """
        content_map = {a[ArtifactKeys.ID]: a[ArtifactKeys.CONTENT] for a in args.get_concept_artifacts() + args.get_query_artifacts()}
        embeddings_manager = EmbeddingsManager(content_map, create_embeddings_on_init=True)

        artifact2match = PredictEntityStep._create_artifact2match(state.direct_matches)

        # Create Prompts
        builders, prompts = self._create_prompts(
            args.llm_manager.prompt_args,
            args,
            artifact2match,
            embeddings_manager
        )

        # Complete Prompts
        message_prompts = [p[PromptKeys.PROMPT] for p in prompts]
        system_prompts = [p[PromptKeys.SYSTEM] for p in prompts]
        prediction_output = LLMTrainer.predict_from_prompts(llm_manager=args.llm_manager,
                                                            prompt_builders=builders,
                                                            message_prompts=message_prompts,
                                                            system_prompts=system_prompts)

        # Parse Responses
        state.predicted_matches = self._parse_responses(prediction_output,
                                                        args,
                                                        builders,
                                                        artifact2match)
        print("hi")

    @staticmethod
    def _create_prompts(llm_args: LLMPromptBuildArgs,
                        args: ConceptArgs,
                        artifact2match: Dict[str, List[str]],
                        embeddings_manager: EmbeddingsManager) -> Tuple[List[PromptBuilder], List[str]]:
        """
        Creates prompts
        :param llm_args: Arguments defining how to define prompt.
        :param args: Contains concepts and query artifacts.
        :return:
        """
        builders = []
        prompts = []
        for query_artifact in args.get_query_artifacts():
            builder = PromptBuilder(
                prompts=[
                    MultiArtifactPrompt("Project Concepts and Terminology", build_method=MultiArtifactPrompt.BuildMethod.XML),
                    ArtifactPrompt("# Target Artifact\n\n---"),
                    Prompt("\nFormat your answer using the following format:",
                           response_manager=JSONResponseManager.from_langgraph_model(
                               ExpectedResponse
                           ))
                ],
            )

            query_existing_concepts = artifact2match[query_artifact[ArtifactKeys.ID]]
            query_concepts = [c for c in args.get_concept_artifacts() if c[ArtifactKeys.ID] not in query_existing_concepts]
            query_concepts = PredictEntityStep.get_similar_concepts(embeddings_manager,
                                                                    query_artifact,
                                                                    query_concepts,
                                                                    args.n_concepts_in_prompt)
            prompt = builder.build(llm_args, artifacts=query_concepts, artifact=query_artifact)
            prompt[PromptKeys.SYSTEM] = system_prompt
            builders.append(builder)
            prompts.append(prompt)

        return builders, prompts

    @staticmethod
    def get_similar_concepts(
            embeddings_manager: EmbeddingsManager,
            query_artifact: Artifact,
            concept_artifacts: List[Artifact],
            n_top: int
    ) -> List[Artifact]:
        query_id = query_artifact[ArtifactKeys.ID]
        concept_ids = [c[ArtifactKeys.ID] for c in concept_artifacts]
        similarity_matrix = embeddings_manager.compare_artifacts([query_id], concept_ids)
        sorted_concepts = sorted(zip(concept_artifacts, similarity_matrix[0]), key=lambda x: x[1], reverse=True)
        selected_concepts = [concept for concept, score in sorted_concepts[:n_top]]
        return selected_concepts

    @staticmethod
    def _parse_responses(
            output: TracePredictionOutput,
            args: ConceptArgs,
            builders: List[PromptBuilder],
            artifact2match: Dict[str, List[str]]
    ) -> List[Trace]:
        """
        Parses model output into trace predictions.
        :param output: The output of the model
        :param args: Concept args containing query and concept artifacts.
        :param builders: List of prompt builders.
        :return:
        """
        traces = []
        text2concept = {c[ArtifactKeys.ID].lower(): c[ArtifactKeys.ID] for c in args.get_concept_artifacts()}
        for artifact, builder, prediction in zip(args.get_query_artifacts(), builders, output.predictions):
            prompt_id = builder.prompts[-1].args.prompt_id
            builder_output = prediction[prompt_id]
            previous_matches = artifact2match[artifact[ArtifactKeys.ID]]
            for predicted_concept_id in builder_output["predictions"]:
                predicted_concept_key = predicted_concept_id.lower()
                if predicted_concept_key not in text2concept:
                    print(f"{predicted_concept_key} was predicted but not in concepts...")
                    continue
                concept_id = text2concept[predicted_concept_key]
                if predicted_concept_id not in previous_matches:
                    trace = Trace(
                        source=artifact[ArtifactKeys.ID],
                        target=concept_id,
                        score=1,
                        explanation="llm_predicted_citation"
                    )
                    traces.append(trace)
        return traces

    @staticmethod
    def _create_artifact2match(matches: List[ConceptMatch]):
        artifact2match = defaultdict(list)
        for m in matches:
            artifact2match[m["artifact_id"]].append(m["concept_id"])
        return artifact2match
