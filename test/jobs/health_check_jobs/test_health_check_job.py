from typing import List, Dict

from test.concepts.test_entity_extraction import TestEntityExtraction
from test.concepts.test_entity_matching import TestEntityMatching
from test.tracing.data_test_context import get_dataset_for_context, ARTIFACT_IDS, EXPECTED_CONTEXT_IDS, assert_correct_related_traces
from tgen.common.objects.artifact import Artifact
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.health_check_jobs.health_check_job import HealthCheckJob
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHealthCheckJobJob(BaseJobTest):
    EXPECTED_CONTRADICTION = ARTIFACT_IDS[0]
    EXISTING_CONCEPTS = ["dog", "cat", "fire truck", "car", "vroom"]
    CONCEPT_LAYER_ID = "concept"
    QUERY_CONCEPTS = ["pug", "dog"]
    QUERY_CONTENT = "Pugs aren't cute dogs."
    QUERY_ID = "target"
    EXPECTED_RELATED_ARTIFACTS = EXPECTED_CONTEXT_IDS + EXISTING_CONCEPTS[:2]

    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager):
        """
        Tests that job is completed succesfully.
        """
        task_prompt: Prompt = SupportedPrompts.CONTRADICTIONS_TASK.value
        contradiction_response_tag = task_prompt.get_all_response_tags()[0]
        artifacts = [Artifact(id=e, content="description", layer_id="entity")
                     for e in self.QUERY_CONCEPTS]
        test_entity_df = ArtifactDataFrame(artifacts)
        ai_manager.set_responses([PromptUtil.create_xml(contradiction_response_tag, self.EXPECTED_CONTRADICTION)])
        TestEntityExtraction.mock_entity_extraction(ai_manager, test_entity_df)
        TestEntityMatching.mock_entity_matching(ai_manager, self.QUERY_CONCEPTS[:1])
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        result: HealthCheckResults = job_result.body
        self.assertListEqual(result.conflicting_ids, [self.EXPECTED_CONTRADICTION])
        assert_correct_related_traces(self, result.context_traces, self.EXPECTED_RELATED_ARTIFACTS, self.QUERY_ID)
        direct_matches = [a[ArtifactKeys.ID] for a in result.concept_matches['matches']]
        undefined_matches = [a[ArtifactKeys.ID] for a in result.concept_matches['undefined_entities']]
        for concept in self.QUERY_CONCEPTS:
            if concept in self.EXISTING_CONCEPTS:
                self.assertIn(concept, direct_matches)
            else:
                self.assertIn(concept, undefined_matches)

    def _get_job(self, additional_chats: List[Dict] = None) -> AbstractJob:
        dataset = get_dataset_for_context()
        dataset.artifact_df.add_artifact(a_id=self.QUERY_ID,
                                         content=self.QUERY_CONTENT,
                                         layer_id="artifacts")
        for i, concept in enumerate(self.EXISTING_CONCEPTS):
            dataset.artifact_df.add_artifact(a_id=concept,
                                             content=concept,
                                             layer_id=self.CONCEPT_LAYER_ID)
        return HealthCheckJob(JobArgs(dataset=dataset), req_id=self.QUERY_ID, concept_layer_id=self.CONCEPT_LAYER_ID)
