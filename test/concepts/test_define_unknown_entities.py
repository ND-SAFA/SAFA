from typing import List
from unittest import TestCase

from test.concepts.constants import ConceptData
from test.concepts.test_entity_matching import TestEntityMatching
from test.concepts.utils import create_concept_args, create_concept_state
from tgen.common.util.prompt_util import PromptUtil
from tgen.concepts.steps.create_response_step import CreateResponseStep
from tgen.concepts.steps.define_unknown_entities import DefineUnknownEntitiesStep
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestDefineUnknownEntities(BaseTest):
    @mock_anthropic
    def test_run(self, ai_manager: TestAIManager) -> None:
        """
        Tests the ability to create the final response for concept pipeline.
        :param ai_manager: AI manager used to mock entity matching.
        :return: None
        """

        args = create_concept_args()
        state = create_concept_state(args)

        # Mock pipeline execution assumptions
        DirectConceptMatchingStep().run(args, state)
        state.entity_data_frames = ConceptData.get_entity_dataframes()
        TestEntityMatching.mock_entity_matching(ai_manager)
        EntityMatchingStep().run(args, state)
        CreateResponseStep().run(args, state)
        entity_ids = [ConceptData.Entities.E3, ConceptData.Entities.E4]
        self.mock_entity_definitions(ai_manager, entity_ids=entity_ids, tc=self)
        DefineUnknownEntitiesStep().run(args, state)

        res = state.response

        TestDefineUnknownEntities.verify_response(self, res)

    @staticmethod
    def mock_entity_definitions(ai_manager, entity_ids: List[str], tc=None):
        """
        Mocks response for entity definition.
        :param ai_manager: AI manager.
        :param entity_ids: List of entity ids to mock definitions for.
        :param tc: Test case.
        :return: None
        """
        if entity_ids is None:
            entity_ids = [ConceptData.Entities.E3, ConceptData.Entities.E4]
        ai_manager.add_responses([lambda prompt: TestDefineUnknownEntities.mock_prediction(prompt, tc)
                                  for entity_id in ConceptData.Entities.get_expected_definitions()
                                  if not entity_ids or entity_id in entity_ids])

    @staticmethod
    def mock_prediction(prompt, tc=None):
        """
        Asserts context matches entity.
        :param prompt: The prompt given to LLM.
        :param tc: Test case.
        :return: The mocked response form lLM.
        """
        expected_context_definitions = ConceptData.Entities.get_expected_definitions()

        message_prompt, system_prompt = prompt
        entity_id = message_prompt.splitlines()[-1]
        if tc:
            tc.assertIn(entity_id, expected_context_definitions)
            tc.assertIn(entity_id, system_prompt)
        return PromptUtil.create_xml("definition", expected_context_definitions[entity_id])

    @staticmethod
    def verify_response(tc: TestCase, res: ConceptPipelineResponse) -> None:
        """
        Verifies that response matches expected test data.
        :param tc: Test case used to make assertions.
        :param res: Response to verify.
        :return: None
        """
        undefined_entity_lookup = {e["concept_id"]: e for e in res["undefined_entities"]}
        expected_undefined_entities = ConceptData.Entities.get_undefined_entities()
        expected_context_definitions = ConceptData.Entities.get_expected_definitions()

        for target_artifact_id, expected_undefined_entities in expected_undefined_entities:
            for e in expected_undefined_entities:
                tc.assertIn(e, undefined_entity_lookup)
                undefined_entity = undefined_entity_lookup[e]
                tc.assertIn(target_artifact_id, undefined_entity["artifact_ids"])
                if e in expected_context_definitions:
                    tc.assertEqual(expected_context_definitions[e], undefined_entity["concept_definition"])
