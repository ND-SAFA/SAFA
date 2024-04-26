from typing import Dict, List

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class CreateResponse(AbstractPipelineStep):
    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Defines
        :param args:
        :param state:
        :return:
        """
        loc2match: Dict[int, List[ConceptMatch]] = self.create_loc2match_map(state.direct_matches)
        direct_matches: List[ConceptMatch] = []
        multi_matches = {}
        for loc, matches in loc2match.items():
            if len(matches) == 1:
                direct_matches.append(matches[0])
            else:
                multi_matches[loc] = matches

        # Undefined entities
        direct_matched_entities = set([m["artifact_id"] for m in state.direct_matches])
        predicted_matched_entities = set([t[TraceKeys.SOURCE] for t in state.predicted_matches])
        matched_entities = direct_matched_entities.union(predicted_matched_entities)
        undefined_entities = [e for e in state.entity_df.to_artifacts() if e[ArtifactKeys.ID] not in matched_entities]

        unique_predicted_entities = [t for t in state.predicted_matches if t[TraceKeys.SOURCE] not in direct_matched_entities]

        state.response = ConceptPipelineResponse(
            matches=direct_matches,
            multi_matches=multi_matches,
            predicted_matches=unique_predicted_entities,
            undefined_entities=undefined_entities
        )

    @staticmethod
    def create_loc2match_map(matches: List[ConceptMatch]) -> Dict[int, List[ConceptMatch]]:
        """
        Groups matches based on their location so multiple matches can be identified.
        :param matches: List of ConceptMatch.
        :return: Map of location matched to the matches at that location.
        """
        match_map = {}
        for m in matches:
            loc = m["loc"]
            if loc not in match_map:
                match_map[loc] = []
            match_map[loc].append(m)
        return match_map
