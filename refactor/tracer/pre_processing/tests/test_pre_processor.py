from copy import deepcopy

from test.base_test import BaseTest
from tracer.pre_processing.pre_processing_option import PreProcessingOption
from tracer.pre_processing.pre_processor import PreProcessor
from tracer.pre_processing.replace_words_step import ReplaceWordsStep


class TestPreProcessor(BaseTest):
    TEST_OPTIONS, TEST_PARAMS = BaseTest.PRE_PROCESSING_PARAMS
    TEST_ARTIFACT_CONTENTS = ["This is 1.0 of 2.0 testCases!", "This i$ the other_one"]
    EXPECTED_CONTENTS = ["Esta is 10 of 20 test Cases", "Esta the other uno"]
    BEFORE_STEP = PreProcessingOption.REPLACE_WORDS
    FIRST_STEP = PreProcessingOption.SEPARATE_JOINED_WORDS
    LAST_STEP = PreProcessingOption.FILTER_MIN_LENGTH

    def test_get_ordered_steps(self):
        before_steps, regular_steps = PreProcessor._get_ordered_steps(self.TEST_OPTIONS, **self.TEST_PARAMS)

        self.assertEquals(len(before_steps), 1)
        self.assertEquals(len(regular_steps), 3)

        self.assertIsInstance(before_steps[0], self.BEFORE_STEP.value)
        self.assertIsInstance(regular_steps[0], self.FIRST_STEP.value)

        self.assertIsInstance(regular_steps[len(regular_steps) - 1], self.LAST_STEP.value)

    def test_order_steps(self):
        steps = [PreProcessingOption.SHUFFLE_WORDS.value(), PreProcessingOption.SEPARATE_JOINED_WORDS.value(),
                 PreProcessingOption.REMOVE_UNWANTED_CHARS.value()]
        expected_order = [1, 2, 0]
        ordered_steps = PreProcessor._order_steps(steps)
        for i, step in enumerate(ordered_steps):
            expected_step = steps[expected_order[i]]
            self.assertEqual(step, expected_step)

    def test_get_step_params(self):
        key, val = deepcopy(self.TEST_PARAMS).popitem()
        step_params = PreProcessor._get_step_params(ReplaceWordsStep, word_replace_mappings=self.TEST_PARAMS["word_replace_mappings"])
        self.assertIn(key, step_params)
        self.assertEqual(step_params[key], val)

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
        return PreProcessor(self.TEST_OPTIONS, word_replace_mappings=self.TEST_PARAMS["word_replace_mappings"])
