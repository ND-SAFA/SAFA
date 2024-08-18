from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.util.str_util import StrUtil
from nltk import PorterStemmer
from tqdm import tqdm

from gen.concepts.concept_args import ConceptArgs
from gen.concepts.concept_state import ConceptState
from gen.concepts.types.concept_match import ConceptMatch
from gen.concepts.util.extract_alt_names import extract_alternate_names
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep


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
        self.stemmer = PorterStemmer()  # using lemmatizer over stemmer bc stemmer can add characters reducing matching ability

    def _run(self, args: ConceptArgs, state: ConceptState) -> None:
        """
        Finds any concept that are directly cited in target artifact.
        :param args: Contains concepts and target artifact.
        :param state: Contains running list of matches.
        :return: None
        """
        concept_ids = [a[ArtifactKeys.ID] for a in args.get_concept_artifacts()]
        concept_alt_names = [alt for c, *alt in extract_alternate_names(concept_ids)]  # [(c0_name, c0_name_alt_name1, ...) ,...]
        concepts_stemmed = [self.stemmer.stem(w) for w in concept_ids]

        matches = []

        # only need to lemmatize concepts, then store those.

        for artifact in tqdm(args.get_query_artifacts(), desc="Finding direct concept matches"):
            target_artifact_content = artifact[ArtifactKeys.CONTENT]
            artifact_id = artifact[ArtifactKeys.ID]

            for c_id, c_alt, c_stem in zip(concept_ids, concept_alt_names, concepts_stemmed):

                start_loc, end_loc = self._find_match(target_artifact_content, c_id, c_stem, *c_alt)
                if start_loc is not None:
                    concept_match = ConceptMatch(
                        artifact_id=artifact_id,
                        concept_id=c_id,
                        start_loc=start_loc,
                        end_loc=end_loc,
                        matched_content=target_artifact_content[start_loc: end_loc]
                    )
                    matches.append(concept_match)

        state.direct_matches = matches

    @staticmethod
    def _find_match(text: str, *matches: str):
        for match in matches:
            start_loc, end_loc = StrUtil.find_start_and_end_loc(text, match, ignore_case=True)
            if start_loc > -1:
                return start_loc, end_loc
        return None, None
