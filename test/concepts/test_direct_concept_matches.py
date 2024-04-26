from test.concepts.utils import create_concept_args
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.direct_concept_matches import DirectConceptMatches
from tgen.concepts.util.extract_alt_names import extract_alternate_names
from tgen.testres.base_tests.base_test import BaseTest


class TestDirectConceptMatches(BaseTest):
    N_MATCHES = 3

    def test_direct_concept_matches(self):
        """
        Verifies that concept are matched via lemmatized words.
        """
        args = create_concept_args()
        step = DirectConceptMatches()

        state = ConceptState()
        step.run(args, state)

        self.assertEqual(self.N_MATCHES, len(state.direct_matches))

        match0 = state.direct_matches[0]
        self.assertEqual("GS", match0["artifact_id"])

        match1 = state.direct_matches[1]
        self.assertEqual("Command", match1["artifact_id"])

        match2 = state.direct_matches[2]
        self.assertEqual("Telemetry (TLM)", match2["artifact_id"])

    def test_alt_name_extraction(self):
        """
        Tests ability to extract alt names defined in parenthesis.
        """
        name1 = "first (alt) last"
        output1 = extract_alternate_names([name1])[0]
        self.assertEqual(output1[0], "first last")
        self.assertEqual(output1[1], "alt")
