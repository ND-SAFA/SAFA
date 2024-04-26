from typing import Dict, List

from nltk import WordNetLemmatizer

from tgen.concepts.concept_args import ConceptArgs
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.types.concept_match import ConceptMatch
from tgen.concepts.util.extract_alt_names import extract_alternate_names
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


def create_concept_artifact_map(concept_names: List[str]) -> Dict:
    """
    Creates map of concept name to list of matching names.
    :param concept_names: List of concept names possible containing alternate names.
    :return: Map of concept artifact id to matching names.
    """
    full_name_list = extract_alternate_names(concept_names)
    concept_map = {}  # maps id in flattened list to id in concept list
    for concept_index, full_concept_names in enumerate(full_name_list):
        concept_name = concept_names[concept_index]
        concept_map[concept_name] = full_concept_names
    return concept_map


class DirectConceptMatches(AbstractPipelineStep):

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
        concept_df = args.concept_df
        target_artifact = args.artifact
        target_artifact_content = target_artifact[ArtifactKeys.CONTENT]

        concept_artifact_ids = concept_df.index.to_list()
        artifact_id2matching_words = create_concept_artifact_map(concept_artifact_ids)

        matches = []
        for concept_artifact_id, (concept_name, *concept_acronyms) in artifact_id2matching_words.items():
            match_index = self._find_match(target_artifact_content, concept_name, concept_acronyms)
            if match_index > -1:
                matches.append(ConceptMatch(artifact_id=concept_artifact_id, loc=match_index))

        state.direct_matches = matches

    def _find_match(self, artifact_content: str, concept_name: str, acronyms: List[str]) -> int:
        """
        Attempts to find direct reference to main name or acronyms in context.
        :param artifact_content: Content of artifact to find concepts in.
        :param concept_name: Name of concept to lemmatize and find in artifact content.
        :param acronyms: List of acronyms to find in artifact content
        :return: Index of where concept is found.
        """
        concept_name = self.lemmatize(concept_name)
        main_index = artifact_content.lower().find(concept_name)
        if main_index > -1:
            return main_index
        for m_str in acronyms:
            str_index = artifact_content.find(m_str)
            if str_index == -1:
                continue
            return str_index
        return -1

    def lemmatize(self, concept: str) -> str:
        """
        Lemmatizes each word in given concept removing punctuation from each word.
        :param concept: The word to sanitize.
        :return: String with each word lemmatize.
        """
        concept_words = concept.lower().split(" ")
        lemmatized_words = [self.lemmatizer.lemmatize(w) for w in concept_words]
        return " ".join(lemmatized_words)
