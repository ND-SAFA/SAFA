from typing import List

from tgen_test.concepts.constants import ConceptData
from tgen_test.concepts.utils import create_concept_args
from tgen.common.objects.artifact import Artifact
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.predict_entity_step import PredictEntityStep
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from tgen.prompts.supported_prompts.concept_prompts import create_entity_extraction_response
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager


class TestPredictEntityStep(BaseTest):

    def test_entity_extraction_with_stanza(self) -> None:
        """
        Verifies that entities are extracted correctly and saved to state.
        """
        args = create_concept_args()
        args.use_llm_for_entity_extraction = False

        step = PredictEntityStep()

        state = ConceptState()
        step.run(args, state)

        entity_batches = [['GS', 'GS Antenna', 'GOES-N', 'GOES-R'], ['SSP']]
        self.assertEqual(len(entity_batches), len(state.entity_data_frames))
        for entity_batch, entity_df in zip(entity_batches, state.entity_data_frames):
            self.verify_entity_df(entity_batch, entity_df)

    @mock_anthropic
    def test_entity_extraction(self, ai_manager: TestAIManager) -> None:
        """
        Verifies that entities are extracted correctly and saved to state.
        """
        entity_dataframes = ConceptData.get_entity_dataframes()
        args = create_concept_args()

        for entity_df in entity_dataframes:
            self.mock_entity_extraction(ai_manager, entity_df)

        step = PredictEntityStep()

        state = ConceptState()
        step.run(args, state)

        entity_batches = ConceptData.get_entity_batches()
        self.assertEqual(len(entity_batches), len(state.entity_data_frames))
        for entity_batch, entity_df in zip(entity_batches, state.entity_data_frames):
            self.verify_entity_df(entity_batch, entity_df)

    def verify_entity_df(self, expected_entities: List[str], entity_df: ArtifactDataFrame) -> None:
        """
        Verifies that entity data frame contains exactly the expected entities.
        :param expected_entities: Entities expected to be be contained in data frame.
        :param entity_df: Data frame containing entities resulting from entity extraction test.
        :return: None
        """
        self.assertEqual(len(expected_entities), len(entity_df))
        resulting_entities = set(entity_df.index)
        expected_entities = set(expected_entities)
        self.assertEqual(expected_entities, resulting_entities)

    @staticmethod
    def mock_entity_extraction(ai_manager: TestAIManager, entity_df: ArtifactDataFrame) -> None:
        """
        Mocks response for entity extraction.
        :param ai_manager: AI manager.
        :param entity_df: Contains entity artifacts.
        :return: None
        """
        response = "".join([TestPredictEntityStep.format_entity(e) for e in entity_df.to_artifacts()])
        ai_manager.add_responses([response])

    @staticmethod
    def format_entity(artifact: Artifact) -> str:
        """
        Creates response XML for entity extraction.
        :param artifact: The entity to create XML response for.
        :return: String representing response.
        """
        entity_name = artifact[ArtifactKeys.ID]
        return create_entity_extraction_response(entity_name)
