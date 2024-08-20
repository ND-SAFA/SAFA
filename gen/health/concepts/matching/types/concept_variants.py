from nltk import PorterStemmer

from gen.health.concepts.matching.concept_matching_util import extract_alternate_names

STEMMER = PorterStemmer()  # using lemmatizer over stemmer bc stemmer can add characters reducing matching ability


class ConceptVariants:
    def __init__(self, concept_id: str):
        """
        Splits the concept id into its components: base_concept, alternative names, and stemmed base concept.
        :param concept_id: The id of the concept.
        :param stemmer: The stemmer used to stem artifacts.
        """
        base_concept, *alt_names = extract_alternate_names([concept_id])[0]
        self.concept_id = concept_id
        self.base_concept = base_concept
        self.alt_names = alt_names
        self.stemmed = STEMMER.stem(base_concept)
