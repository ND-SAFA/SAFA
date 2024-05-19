from typing import List, Tuple

from nltk import WordNetLemmatizer

from tgen.common.constants.deliminator_constants import SPACE
from tgen.common.util.str_util import StrUtil
from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.util.extract_alt_names import extract_alternate_names
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


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

    def __init__(self):
        """
        Initializes a common lemmatizer.
        """
        self.lemmatizer = WordNetLemmatizer()  # using lemmatizer over stemmer bc stemmer can add characters reducing matching ability

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Finds any concept that are directly cited in target artifact.
        :param args: Contains concepts and target artifact.
        :param state: Contains running list of matches.
        :return: None
        """
        concept_artifact_ids = state.concept_df.index.to_list()
        matches = []

        for artifact in args.artifacts:
            target_artifact_content = artifact[ArtifactKeys.CONTENT]
            artifact_id = artifact[ArtifactKeys.ID]
            concept_alternate_names = extract_alternate_names(concept_artifact_ids)  # [(c0_name, c0_name_alt_name1, ...) ,...]

            for concept_index, (main_name, *alternate_names) in enumerate(concept_alternate_names):
                start_loc, end_loc = self._find_match(target_artifact_content, main_name, alternate_names)
                if start_loc == -1:
                    continue
                concept_match = ConceptMatch(
                    artifact_id=artifact_id,
                    concept_id=concept_artifact_ids[concept_index],
                    start_loc=start_loc,
                    end_loc=end_loc,
                    matched_content=target_artifact_content[start_loc: end_loc]
                )
                matches.append(concept_match)

        state.direct_matches = matches

    def _find_match(self, artifact_content: str, main_name: str, alternate_names: List[str]) -> Tuple[int, int]:
        """
        Attempts to find lemmatized reference to main name or direct reference to alternate names.
        :param artifact_content: Content of artifact to find concepts in.
        :param main_name: Name of concept to lemmatize and find in artifact content.
        :param alternate_names: List of acronyms to find in artifact content
        :return: Index of where concept is found. -1 if none found.
        """
        main_start, main_end = StrUtil.find_start_and_end_loc(artifact_content, main_name, ignore_case=True)
        if main_start > -1:
            return main_start, main_end
        lemmatized = self.lemmatize(main_name)
        for m_str in [lemmatized] + alternate_names:
            str_start, str_end = StrUtil.find_start_and_end_loc(artifact_content, m_str, ignore_case=False)
            if str_start == -1:
                continue

            return str_start, str_end
        return -1, -1

    def lemmatize(self, concept: str) -> str:
        """
        Lemmatizes each word in given concept removing punctuation from each word.
        :param concept: The word to sanitize.
        :return: String with each word lemmatize.
        """
        if concept.isupper():
            # If is ancronym, then match start of new word + acronym (lower case is used to match later)
            return SPACE + concept.lower()
        concept_words = concept.lower().split(SPACE)
        lemmatized_words = [self.lemmatizer.lemmatize(w) for w in concept_words]
        return SPACE.join(lemmatized_words)
