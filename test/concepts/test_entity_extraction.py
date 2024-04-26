from test.concepts.utils import create_concept_args, create_concept_test_entities
from tgen.common.objects.artifact import Artifact
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.extract_artifact_entities import EntityExtraction
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestEntityExtraction(BaseTest):
    @mock_openai
    def test_entity_extraction(self, ai_manager: TestAIManager) -> None:
        """
        Verifies that entities are extracted correctly and saved to state.
        """
        test_entity_df = create_concept_test_entities()

        args = create_concept_args()
        step = EntityExtraction()

        state = ConceptState()
        step.run(args, state)

        entity_df = state.entity_df
        self.assertEqual(len(test_entity_df), len(entity_df))
        for i in range(len(test_entity_df)):
            self.assertEqual(test_entity_df.iloc[i].to_dict(), entity_df.iloc[i].to_dict())

    @staticmethod
    def mock_entity_extraction(ai_manager: TestAIManager, entity_df: ArtifactDataFrame) -> None:
        """
        Mocks response for entity extraction.
        :param ai_manager: AI manager.
        :param entity_df: Contains entity artifacts.
        :return: None
        """
        response = "".join([TestEntityExtraction.format_entity(e) for e in entity_df.to_artifacts()])
        ai_manager.add_responses([response])

    @staticmethod
    def format_entity(artifact: Artifact) -> str:
        """
        Creates response XML for entity extraction.
        :param artifact: The entity to create XML response for.
        :return: String representing response.
        """
        entity_name = artifact[ArtifactKeys.ID]
        entity_description = artifact[ArtifactKeys.CONTENT]
        return (f"<{EntityExtraction.ENTITY_TAG}>"
                f"<{EntityExtraction.ENTITY_NAME_TAG}>{entity_name}</{EntityExtraction.ENTITY_NAME_TAG}>"
                f"<{EntityExtraction.ENTITY_DESCRIPTION_TAG}>{entity_description}</{EntityExtraction.ENTITY_DESCRIPTION_TAG}>"
                f"</{EntityExtraction.ENTITY_TAG}>")
