from typing import Type

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from gen_common.data.processing.cleaning.data_cleaner import DataCleaner
from gen_common.data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
from gen_common_test.base_tests.base_test import BaseTest


class TestDataCleaner(BaseTest):
    TEST_ARTIFACT_CONTENTS = ["This is 1.0 of 2.0 testCases!", "This is the other_one"]
    EXPECTED_CONTENTS = ["Esta is 1.0 of 2.0 test Cases!", "Esta is the other uno"]
    BEFORE_STEP: Type[AbstractDataProcessingStep] = SupportedDataCleaningStep.REPLACE_WORDS.value
    FIRST_STEP: Type[AbstractDataProcessingStep] = SupportedDataCleaningStep.SEPARATE_JOINED_WORDS.value
    LAST_STEP: Type[AbstractDataProcessingStep] = SupportedDataCleaningStep.FILTER_MIN_LENGTH.value

    def test_order_steps(self):
        steps = [SupportedDataCleaningStep.SHUFFLE_WORDS.value(),
                 SupportedDataCleaningStep.SEPARATE_JOINED_WORDS.value(),
                 SupportedDataCleaningStep.REMOVE_UNWANTED_CHARS.value()]
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
        return self.DATA_CLEANER
