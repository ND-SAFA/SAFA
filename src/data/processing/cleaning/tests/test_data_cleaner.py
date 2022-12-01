from typing import Type

from test.base_test import BaseTest
from data.processing.cleaning.data_cleaning_steps import DataCleaningSteps
from data.processing.cleaning.data_cleaner import DataCleaner
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class TestDataCleaner(BaseTest):
    TEST_ARTIFACT_CONTENTS = ["This is 1.0 of 2.0 testCases!", "This i$ the other_one"]
    EXPECTED_CONTENTS = ["Esta is 10 of 20 test Cases", "Esta the other uno"]
    BEFORE_STEP: Type[AbstractDataProcessingStep] = DataCleaningSteps.REPLACE_WORDS.value
    FIRST_STEP: Type[AbstractDataProcessingStep] = DataCleaningSteps.SEPARATE_JOINED_WORDS.value
    LAST_STEP: Type[AbstractDataProcessingStep] = DataCleaningSteps.FILTER_MIN_LENGTH.value

    def test_order_steps(self):
        steps = [DataCleaningSteps.SHUFFLE_WORDS.value(), DataCleaningSteps.SEPARATE_JOINED_WORDS.value(),
                 DataCleaningSteps.REMOVE_UNWANTED_CHARS.value()]
        expected_order = [1, 2, 0]
        ordered_steps = DataCleaner._order_steps(steps)
        for i, step in enumerate(ordered_steps):
            expected_step = steps[expected_order[i]]
            self.assertEqual(step, expected_step)

    def test_run(self):
        data_cleaner = self.get_data_cleaner()
        processed_content = data_cleaner.run(self.TEST_ARTIFACT_CONTENTS)
        self.assertListEqual(processed_content, self.EXPECTED_CONTENTS)

    def get_data_cleaner(self):
        return DataCleaner(self.DATA_CLEANING_STEPS)
