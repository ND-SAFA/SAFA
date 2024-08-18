from gen_test.concepts.constants import CONCEPT_R1, ConceptData
from gen_test.concepts.utils import create_concept_args, create_concept_state
from gen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from gen.concepts.util.extract_alt_names import extract_alternate_names
from gen_common_test.base.tests.base_test import BaseTest


class TestDirectConceptMatching(BaseTest):

    def test_direct_concept_matches(self):
        """
        Verifies that concept are matched via lemmatized words.
        """
        args = create_concept_args()
        step = DirectConceptMatchingStep()

        state = create_concept_state(args)
        step.run(args, state)

        self.assertEqual(len(ConceptData.DirectMatches), len(state.direct_matches))

        for expected, result in zip(ConceptData.DirectMatches, state.direct_matches):
            self.assertEqual(CONCEPT_R1, result["artifact_id"])
            self.assertEqual(expected, result["concept_id"])

    def test_alt_name_extraction(self):
        """
        Tests ability to extract alt names defined in parenthesis.
        """
        name1 = "first (alt) last"
        output1 = extract_alternate_names([name1])[0]
        self.assertEqual(output1[0], "first last")
        self.assertEqual(output1[1], "alt")
