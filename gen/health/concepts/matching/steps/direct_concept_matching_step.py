from typing import List, Tuple

from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.util.str_util import StrUtil
from tqdm import tqdm

from gen.health.concepts.matching.types.concept_direct_match import ConceptDirectMatch
from gen.health.concepts.matching.types.concept_variants import ConceptVariants
from gen.health.health_args import HealthArgs
from gen.health.health_state import HealthState


class DirectConceptMatchingStep(AbstractPipelineStep):
    """
    Attempts to find all concepts that are referenced in the artifact content.

    # Concepts
    Each concept is an artifact where its name is the ID and the definition of the concept is the content.
    The concept ID is used to see if it is cited in the text.

    # Example
    - Concept = Telemetry (TLM): The automatic measurement and wireless transmission of data from remote sources.
    - Artifact = ... transmit command and data signals to, and receive telemetry and rebroadcast data ...

    The ID must be separated into parts which we call the main_name and alternate names.

    1. Main name is lemmatized and searched for in artifact. Return if found.
    2. Else, alternate names are searched as is since they are assumed to be the short form of the artifact (e.g. acronym)

    * Typically, alternate names are just acronyms, but we reserve the use of parenthesis.
    * This functionality will be fixed at a future date but allows as an easy way to define alternate names.
    """

    def _run(self, args: HealthArgs, state: HealthState) -> None:
        """
        Finds any concept that are directly cited in target artifact.
        :param args: Contains concepts and target artifact.
        :param state: Contains running list of matches.
        :return: None
        """
        concept_proxies = [ConceptVariants(a[ArtifactKeys.ID]) for a in args.get_concept_artifacts()]
        matches = []

        for artifact in tqdm(args.get_query_artifacts(), desc="Finding direct concept matches"):
            artifact_matches = self.find_matches_in_artifact(artifact, concept_proxies)
            matches.extend(artifact_matches)

        state.direct_matches = matches

    @staticmethod
    def find_matches_in_artifact(artifact: Artifact, concept_variants: List[ConceptVariants]) -> List[ConceptDirectMatch]:
        """
        Calculates if any concept matches are directly matched in artifact.
        :param artifact: The artifact whose content is searched for direct matches.
        :param concept_variants: List of concepts in project alongside all of its possible variants.
        :return: List of matches found in artifact.
        """
        matches = []
        target_artifact_content = artifact[ArtifactKeys.CONTENT]
        artifact_id = artifact[ArtifactKeys.ID]
        for concept_proxy in concept_variants:
            start_loc, end_loc = DirectConceptMatchingStep.find_concept_usages(target_artifact_content, concept_proxy)
            if start_loc is not None:
                concept_match = ConceptDirectMatch(
                    artifact_id=artifact_id,
                    concept_id=concept_proxy.concept_id,
                    start_loc=start_loc,
                    end_loc=end_loc,
                    matched_content=target_artifact_content[start_loc: end_loc]
                )
                matches.append(concept_match)
        return matches

    @staticmethod
    def find_concept_usages(content: str, concept_variants: ConceptVariants) -> Tuple[int, int]:
        """
        Finds usage of concept (or variants) in content.
        :param content: The content to search within.
        :param concept_variants: The concept (and variants) to search for.
        :return: Start and end location of match if found, otherwise None for start and end loc.
        """
        return DirectConceptMatchingStep._find_match_locations(
            content,
            concept_variants.base_concept, concept_variants.stemmed, *concept_variants.alt_names
        )

    @staticmethod
    def _find_match_locations(text: str, *matches: str):
        """
        Finds locations for first successful match in text.
        :param text: The text to look inside of.
        :param matches: Variable arguments each of which is considered a potential match.
        :return: Start and end location of where the match was found in the text.
        """
        for match in matches:
            start_loc, end_loc = StrUtil.find_start_and_end_loc(text, match, ignore_case=True)
            if start_loc > -1:
                return start_loc, end_loc
        return None, None
