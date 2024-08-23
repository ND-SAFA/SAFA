from abc import ABC, abstractmethod
from typing import List, Tuple
from unittest import TestCase

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.mock.test_ai_manager import TestAIManager

from gen.health.health_state import HealthState


class HealthTaskVerifier(ABC):
    @abstractmethod
    def get_test_data(self) -> Tuple[PromptDataset, List[str]]:
        """
        :return: Test dataset and query ids.
        """

    @abstractmethod
    def mock_responses(self, ai_manager: TestAIManager, chat_manager: TestResponseManager) -> None:
        """
        Mocks responses needed for task.
        :param ai_manager: The response manager to add responses to.
        :param chat_manager: Response manager used for mocking chat messages.
        :return: None
        """

    @abstractmethod
    def verify_state(self, tc: TestCase, state: HealthState) -> None:
        """
        Verifies that state contains expected entities.
        :param tc: Test case used to make assertions.
        :param state: The health state after task has been performed.
        :return:None
        """
