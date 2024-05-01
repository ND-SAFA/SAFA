from test.concepts.constants import ConceptData
from test.concepts.utils import create_concept_args, create_concept_state
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.util.extract_alt_names import extract_alternate_names
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest


class TestDirectConceptMatching(BaseTest):

    def test_direct_concept_matches(self):
        """
        Verifies that concept are matched via lemmatized words.
        """
        args = create_concept_args()
        step = DirectConceptMatchingStep()

        state = create_concept_state(args)
        step.run(args, state)

        direct_matches = ConceptData.DirectMatches
        self.assertEqual(len(direct_matches), len(state.direct_matches))

        for expected, result in zip(direct_matches, state.direct_matches):
            self.assertEqual(expected, result[ArtifactKeys.ID])

    def test_alt_name_extraction(self):
        """
        Tests ability to extract alt names defined in parenthesis.
        """
        name1 = "first (alt) last"
        output1 = extract_alternate_names([name1])[0]
        self.assertEqual(output1[0], "first last")
        self.assertEqual(output1[1], "alt")
