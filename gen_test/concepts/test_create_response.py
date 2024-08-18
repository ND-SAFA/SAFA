from gen.concepts.steps.create_response_step import CreateResponseStep
from gen.concepts.types.concept_match import ConceptMatch
from gen_common_test.base.tests.base_test import BaseTest


class TestCreateResponse(BaseTest):

    def test_multi_match(self):
        start_loc = 5
        matches = [
            ConceptMatch(artifact_id="a1", concept_id="c1", start_loc=15, end_loc=20, matched_content=""),
            ConceptMatch(artifact_id="a1", concept_id="c2", start_loc=start_loc, end_loc=10, matched_content=""),
            ConceptMatch(artifact_id="a1", concept_id="c3", start_loc=start_loc, end_loc=10, matched_content="")
        ]
        direct_matches, multi_matches = CreateResponseStep.analyze_matches(matches)
        self.assertEqual(1, len(direct_matches))
        self.assertEqual(1, len(multi_matches))
        multi_match_children = multi_matches["a1"][start_loc]
        self.assertEqual(2, len(multi_match_children))
        multi_match_concepts = set([m["concept_id"] for m in multi_match_children])
        self.assertEqual({"c2", "c3"}, multi_match_concepts)
