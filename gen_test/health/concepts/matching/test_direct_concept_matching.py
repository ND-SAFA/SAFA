from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.matching.concept_matching_state import ConceptMatchingState
from gen.health.concepts.matching.concept_matching_util import extract_alternate_names
from gen.health.concepts.matching.steps.direct_concept_matching_step import DirectConceptMatchingStep
from gen_test.health.concepts.matching.constants import CONCEPT_R1, ConceptData
from gen_test.health.concepts.matching.utils import create_concept_args


class TestDirectConceptMatching(BaseTest):

    def test_direct_concept_matches(self):
        """
        Verifies that concept are matched via lemmatized words.
        """
        args = create_concept_args()
        step = DirectConceptMatchingStep()

        state = ConceptMatchingState()
        step.run(args, state)

        self.verify_state(self, state)

    @staticmethod
    def verify_state(self, state: ConceptMatchingState):
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
