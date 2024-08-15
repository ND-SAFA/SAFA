from collections import defaultdict
from typing import Dict, List, Tuple

from tgen.concepts.types.concept_match import ConceptMatch


class CreateResponseStep:

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
