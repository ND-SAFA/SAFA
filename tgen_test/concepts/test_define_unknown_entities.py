from typing import Dict
from unittest import TestCase

from tgen_test.concepts.constants import ConceptData
from tgen_test.concepts.test_entity_matching import TestEntityMatching
from tgen_test.concepts.utils import create_concept_args, create_concept_state
from common_resources.tools.util.prompt_util import PromptUtil
from tgen.concepts.steps.create_response_step import CreateResponseStep
from tgen.concepts.steps.define_unknown_entities import DefineUnknownEntitiesStep
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager


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

        # Capture currently undefined entities.

        undefined_entities = state.response["undefined_entities"]
        entity_ids = [e["concept_id"] for e in undefined_entities]
        entity_definitions = {e["concept_id"]: self.create_mock_def(e['concept_id']) for e in undefined_entities}

        # Execute step
        self.mock_entity_definitions(ai_manager, entity_definitions, tc=self)
        DefineUnknownEntitiesStep().run(args, state)

        res = state.response

        TestDefineUnknownEntities.verify_response(self, res)

    @staticmethod
    def create_mock_def(concept_id: str):
        return f"{concept_id} definition"

    @staticmethod
    def mock_entity_definitions(ai_manager, entity_definitions: Dict[str, str], tc=None):
        """
        Mocks response for entity definition.
        :param ai_manager: AI manager.
        :param entity_definitions: Definitions to mock.
        :param tc: Test case.
        :return: None
        """
        responses = [PromptUtil.create_xml("definition", e_def) for e_id, e_def in entity_definitions.items()]
        ai_manager.add_responses(responses)

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
        expected_context_definitions = {e["concept_id"]: TestDefineUnknownEntities.create_mock_def(e["concept_id"])
                                        for e in res["undefined_entities"]}

        for undefined_entity in res["undefined_entities"]:
            concept_id = undefined_entity["concept_id"]
            expected_definition = expected_context_definitions[concept_id]
            tc.assertEqual(undefined_entity["concept_definition"], expected_definition)
