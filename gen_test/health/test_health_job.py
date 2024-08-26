from gen_common_test.base.tests.base_test import BaseTest

from gen.health.types.health_tasks import HealthTask
from gen_test.health.health_test_runner import run_health_test_case
from gen_test.health.verifiers.concept_extraction_verifier import ConceptExtractionVerifier
from gen_test.health.verifiers.concept_matching_verifier import ConceptMatchingVerifier
from gen_test.health.verifiers.contradiction_verifier import ContradictionsVerifier


class TestHealthJob(BaseTest):
    def test_contradiction_task(self):
        run_health_test_case(self,
                             HealthTask.CONTRADICTION,
                             ContradictionsVerifier())

    def test_concept_extraction(self):
        run_health_test_case(self,
                             HealthTask.CONCEPT_EXTRACTION,
                             ConceptExtractionVerifier())

    def test_concept_matching(self):
        run_health_test_case(self,
                             HealthTask.CONCEPT_MATCHING,
                             ConceptMatchingVerifier())
