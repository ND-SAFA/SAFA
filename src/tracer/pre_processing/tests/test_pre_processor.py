from typing import Type

from test.base_test import BaseTest
from tracer.pre_processing.pre_processing_steps import PreProcessingSteps
from tracer.pre_processing.pre_processor import PreProcessor
from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep


class TestPreProcessor(BaseTest):
    TEST_ARTIFACT_CONTENTS = ["This is 1.0 of 2.0 testCases!", "This i$ the other_one"]
    EXPECTED_CONTENTS = ["Esta is 10 of 20 test Cases", "Esta the other uno"]
    BEFORE_STEP: Type[AbstractPreProcessingStep] = PreProcessingSteps.REPLACE_WORDS.value
    FIRST_STEP: Type[AbstractPreProcessingStep] = PreProcessingSteps.SEPARATE_JOINED_WORDS.value
    LAST_STEP: Type[AbstractPreProcessingStep] = PreProcessingSteps.FILTER_MIN_LENGTH.value

    def test_get_ordered_steps(self):
        before_steps, regular_steps = PreProcessor._get_ordered_steps(BaseTest.PRE_PROCESSING_STEPS)

        self.assertEquals(len(before_steps), 1)
        self.assertEquals(len(regular_steps), 3)

        self.assertIsInstance(before_steps[0], self.BEFORE_STEP)
        self.assertIsInstance(regular_steps[0], self.FIRST_STEP)

        self.assertIsInstance(regular_steps[len(regular_steps) - 1], self.LAST_STEP)

    def test_order_steps(self):
        steps = [PreProcessingSteps.SHUFFLE_WORDS.value(), PreProcessingSteps.SEPARATE_JOINED_WORDS.value(),
                 PreProcessingSteps.REMOVE_UNWANTED_CHARS.value()]
        expected_order = [1, 2, 0]
        ordered_steps = PreProcessor._order_steps(steps)
        for i, step in enumerate(ordered_steps):
            expected_step = steps[expected_order[i]]
            self.assertEqual(step, expected_step)

    def test_get_word_list(self):
        test_content = "This is a test"
        word_list = PreProcessor._get_word_list(test_content)
        self.assertIsInstance(word_list, list)

    def test_reconstruct_content(self):
        test_word_list = ["This", "is", "a", "test"]
        content = PreProcessor._reconstruct_content(test_word_list)
        self.assertIsInstance(content, str)

    def test_run(self):
        pre_processor = self.get_test_pre_processor()
        processed_content = pre_processor.run(self.TEST_ARTIFACT_CONTENTS)
        self.assertListEqual(processed_content, self.EXPECTED_CONTENTS)

    def get_test_pre_processor(self):
        return PreProcessor(self.PRE_PROCESSING_STEPS)
