from typing import Dict, List

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.objects.artifact import Artifact
from gen_common.jobs.abstract_job import AbstractJob, JobResult
from gen_common.jobs.job_args import JobArgs
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_job_test import BaseJobTest

from gen.health.contradiction.contradiction_prompts import create_contradiction_response
from gen.health.health_job import HealthCheckJob
from gen.health.health_results import HealthResults
from gen_test.health.concepts.extraction.concept_extraction_test_constants import TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION, \
    TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
from gen_test.health.concepts.extraction.test_define_undefined_concepts_step import TestDefineUndefinedConceptsStep
from gen_test.health.concepts.extraction.test_undefined_concept_extraction_step import TestUndefinedConceptExtractionStep
from gen_test.health.health_check_constants import CONCEPT_LAYER_ID, EXISTING_CONCEPTS, EXPECTED_CONFLICTING_IDS, \
    EXPECTED_CONTRADICTION_EXPLANATION, \
    QUERY_CONCEPTS, QUERY_CONTENT, QUERY_ID
from gen_test.health.health_check_utils import assert_health_check_success, get_dataset_for_context


class TestHealthJob(BaseJobTest):

    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager):
        """
        Tests that job is completed successfully.
        """
        self.mock_responses(ai_manager)
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        result: HealthResults = job_result.body
        assert_health_check_success(self, result)

    def _get_job(self, additional_chats: List[Dict] = None) -> AbstractJob:
        dataset = self.get_dataset_for_health_checks()
        return HealthCheckJob(
            JobArgs(dataset=dataset),
            query_ids=[QUERY_ID],
            concept_layer_id=CONCEPT_LAYER_ID
        )

    @staticmethod
    def mock_responses(ai_manager):
        # Setup: Dataset
        artifacts = [Artifact(id=e, content="description", layer_id="entity")
                     for e in QUERY_CONCEPTS]
        test_entity_df = ArtifactDataFrame(artifacts)

        # Mock: Contradictions
        ai_manager.add_responses([
            create_contradiction_response(
                EXPECTED_CONTRADICTION_EXPLANATION, EXPECTED_CONFLICTING_IDS)]
        )
        # Mock: Unknown Entity Extraction
        ai_manager.add_responses([
            TestUndefinedConceptExtractionStep.create_mock_response(
                TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
            ),
            TestDefineUndefinedConceptsStep.create_mock_response(
                TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION
            )
        ])

    @staticmethod
    def get_dataset_for_health_checks():
        dataset = get_dataset_for_context()
        dataset.artifact_df.add_artifact(id=QUERY_ID,
                                         content=QUERY_CONTENT,
                                         layer_id="artifacts")
        for i, concept in enumerate(EXISTING_CONCEPTS):
            dataset.artifact_df.add_artifact(id=concept,
                                             content=concept,
                                             layer_id=CONCEPT_LAYER_ID)
        return dataset
