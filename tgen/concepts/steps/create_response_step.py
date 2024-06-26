from collections import defaultdict
from typing import Dict, List, Set, Tuple

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.concepts.types.entity_matching_pred import EntityMatchingPred
from tgen.concepts.types.undefined_concept import UndefinedConcept
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class CreateResponseStep(AbstractPipelineStep):
    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Computes matched entities, ambiguously matched entities (multi-match), predicted entities, and undefined entities.
        :param args: Not used.
        :param state: Used to retrieve intermediate and store final result.
        :return: None
        """
        direct_matches, multi_matches = self.analyze_matches(state.direct_matches)

        # Undefined entities
        direct_matched_entities = set([m["matched_content"] for m in state.direct_matches])
        predicted_matched_entities = set([t["entity_id"] for t in state.predicted_matches])
        predicted_links = [self.to_link(p) for p in state.predicted_matches]
        matched_entities = direct_matched_entities.union(predicted_matched_entities)
        undefined_concepts = self.create_undefined_concepts(args.artifacts, state.entity_data_frames, matched_entities)

        state.response = ConceptPipelineResponse(
            matches=direct_matches,
            multi_matches=multi_matches,
            predicted_matches=predicted_links,
            undefined_entities=undefined_concepts
        )

    @staticmethod
    def analyze_matches(matches: List[ConceptMatch]) -> Tuple[List[ConceptMatch], Dict[str, Dict[int, List[ConceptMatch]]]]:
        """
        Reads direct matches and identifies those that are multi-matches.
        :param matches: The direct matches to separate from multi-matches.
        :return: List of purely direct matches and then list of multi-matches.
        """
        artifact2matches = defaultdict(list)
        for match in matches:
            artifact2matches[match["artifact_id"]].append(match)

        direct_matches: List[ConceptMatch] = []
        multi_matches = {}  # artifact id -> loc -> multi-matches
        for artifact, artifact_matches in artifact2matches.items():
            loc2match: Dict[int, List[ConceptMatch]] = CreateResponseStep.create_loc2match_map(artifact_matches)
            artifact_multi_matches = {}
            for loc, matches in loc2match.items():
                if len(matches) == 1:
                    direct_matches.append(matches[0])
                else:
                    artifact_multi_matches[loc] = matches
            multi_matches[artifact] = artifact_multi_matches
        return direct_matches, multi_matches

    @staticmethod
    def create_undefined_concepts(target_artifacts: List[Artifact], entity_data_frames: List[ArtifactDataFrame],
                                  matched_entities: Set[str]):
        """
        Creates list of undefined concepts for project.
        :param target_artifacts: List of target artifacts.
        :param entity_data_frames: Data frames of entities extracted for each artifact.
        :param matched_entities: Entities IDs who were already matched.
        :return: List of undefined concepts.
        """
        undefined2artifact = {}
        undefined_concept_lookup = {}
        for artifact, entity_df in zip(target_artifacts, entity_data_frames):
            undefined_entities = [e for e in entity_df.to_artifacts() if e[ArtifactKeys.ID] not in matched_entities]

            for e in undefined_entities:
                undefined_concept_id = e[ArtifactKeys.ID]
                DictUtil.initialize_value_if_not_in_dict(undefined2artifact, undefined_concept_id, [])
                undefined2artifact[undefined_concept_id].append(artifact[ArtifactKeys.ID])  # can override matching undefined concepts
                undefined_concept_lookup[undefined_concept_id] = e

        undefined_concepts = []
        for e_id, e in undefined_concept_lookup.items():
            undefined_concepts.append(
                UndefinedConcept(
                    artifact_ids=undefined2artifact[e_id],
                    concept_id=e_id,
                    concept_definition=e[ArtifactKeys.CONTENT]
                )
            )
        return undefined_concepts

    @staticmethod
    def create_loc2match_map(matches: List[ConceptMatch]) -> Dict[int, List[ConceptMatch]]:
        """
        Groups matches based on their location so multiple matches can be identified.
        :param matches: List of ConceptMatch.
        :return: Map of location matched to the matches at that location.
        """
        match_map = {}
        for m in matches:
            loc = m["start_loc"]
            if loc not in match_map:
                match_map[loc] = []
            match_map[loc].append(m)
        return match_map

    @staticmethod
    def to_link(pred: EntityMatchingPred):
        """
        Converts entity match prediction into trace link.
        :param pred: The prediction.
        :return: Trace link between concept and artifact.
        """
        return Trace(
            source=pred["concept_id"],
            target=pred["artifact_id"],
            score=1
        )
