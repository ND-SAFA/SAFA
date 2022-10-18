from test.base_test import BaseTest
from tracer.pre_processing.pre_processing_options import PreProcessingOptions
from tracer.pre_processing.pre_processor import PreProcessor


class TestPreProcessor(BaseTest):
    TEST_OPTIONS = {PreProcessingOptions.REMOVE_UNWANTED_CHARS: True,
                    PreProcessingOptions.REPLACE_WORDS: True,
                    PreProcessingOptions.SEPARATE_JOINED_WORDS: True,
                    PreProcessingOptions.SHUFFLE_WORDS: False,
                    PreProcessingOptions.FILTER_MIN_LENGTH: True}
    TEST_REPLACE_WORD_MAPPINGS = {"This": "Esta", "one": "uno"}
    TEST_ARTIFACT_CONTENTS = ["This is 1.0 of 2.0 testCases!", "This i$ the other_one"]
    EXPECTED_CONTENTS = ["Esta is 10 of 20 test Cases", "Esta the other uno"]
    BEFORE_STEP = PreProcessingOptions.REPLACE_WORDS
    FIRST_STEP = PreProcessingOptions.SEPARATE_JOINED_WORDS
    LAST_STEP = PreProcessingOptions.FILTER_MIN_LENGTH

    def test_get_ordered_steps(self):
        step_params = {PreProcessingOptions.REPLACE_WORDS: {"word_replace_mappings": self.TEST_REPLACE_WORD_MAPPINGS}}
        before_steps, regular_steps = PreProcessor._get_ordered_steps(self.TEST_OPTIONS, step_params)

        self.assertEquals(len(before_steps), 1)
        self.assertEquals(len(regular_steps), 3)

        self.assertIsInstance(before_steps[0], self.BEFORE_STEP.value)
        self.assertIsInstance(regular_steps[0], self.FIRST_STEP.value)

        self.assertIsInstance(regular_steps[len(regular_steps) - 1], self.LAST_STEP.value)

    def test_order_steps(self):
        steps = [PreProcessingOptions.SHUFFLE_WORDS.value(), PreProcessingOptions.SEPARATE_JOINED_WORDS.value(),
                 PreProcessingOptions.REMOVE_UNWANTED_CHARS.value()]
        expected_order = [1, 2, 0]
        ordered_steps = PreProcessor._order_steps(steps)
        for i, step in enumerate(ordered_steps):
            expected_step = steps[expected_order[i]]
            self.assertEqual(step, expected_step)

    def test_get_step_params(self):
        step_params = PreProcessor._get_step_params(word_replace_mappings=self.TEST_REPLACE_WORD_MAPPINGS)
        self.assertIn(PreProcessingOptions.REPLACE_WORDS, step_params)
        self.assertIn("word_replace_mappings", step_params[PreProcessingOptions.REPLACE_WORDS])
        self.assertDictEqual(step_params[PreProcessingOptions.REPLACE_WORDS]["word_replace_mappings"],
                             self.TEST_REPLACE_WORD_MAPPINGS)

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
        return PreProcessor(self.TEST_OPTIONS, word_replace_mappings=self.TEST_REPLACE_WORD_MAPPINGS)
