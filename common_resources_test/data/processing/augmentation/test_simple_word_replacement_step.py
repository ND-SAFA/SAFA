import math

from common_resources_test.base_tests.base_test import BaseTest
from common_resources.data.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep, \
    WordRepresentation
from nltk.corpus import wordnet as wn


class TestSimpleWordReplacementStep(BaseTest):

    def test_run(self):
        step = self.get_word_replacement_step()
        data_entries = [("0", "The city planning is missing in this depressing city"), ("1", "the cars always break"),
                        ("2", "I hate South Bend alot"), ("3", "South Bend is frigid")]
        result = list(step.run(data_entries, 3))
        self.assertEqual(len(result), 3)
        for augmented_data, i in result:
            self.assertEqual(int(data_entries[i][0]), i)

    def test_get_number_to_sample(self):
        self.assertEqual(2, SimpleWordReplacementStep._get_number_to_sample(5, 5, 7))
        self.assertEqual(0, SimpleWordReplacementStep._get_number_to_sample(5, 5, 5))
        self.assertEqual(5, SimpleWordReplacementStep._get_number_to_sample(5, 5, 17))

    def test_augment_content(self):
        orig_content = "The city planning is missing in this depressing city and the cars always break"
        indices2sample = [4, 7, 12, 13]

        self.word_replacement_test(orig_content, indices2sample, 0.15)
        self.word_replacement_test(orig_content, indices2sample, 0.3)

    def test_get_synonyms(self):
        synonyms = {syn.lower() for syn in SimpleWordReplacementStep._get_synonyms("south", "n")}
        self.assertTrue("south" not in synonyms)
        self.assertTrue("southward" in synonyms)

    def test_get_word_pos(self):
        noun = SimpleWordReplacementStep._get_word_pos("NNP")
        self.assertEqual(wn.NOUN, noun)
        verb = SimpleWordReplacementStep._get_word_pos("VBZ")
        self.assertEqual(wn.VERB, verb)
        adj = SimpleWordReplacementStep._get_word_pos("JJ")
        self.assertEqual(wn.ADJ, adj)
        adv = SimpleWordReplacementStep._get_word_pos("RB")
        self.assertEqual(wn.ADV, adv)
        unk = SimpleWordReplacementStep._get_word_pos("PDT")
        self.assertEqual(None, unk)

    def test_to_word_representation(self):
        orig_content = "South Bend is frigid"
        orig_words = orig_content.split()
        word_reps = SimpleWordReplacementStep._to_word_representations(orig_content)
        self.assertEqual(len(orig_words), len(word_reps))
        for i, word in enumerate(orig_words):
            self.assertEqual(word, word_reps[i].word)
            self.assertEqual(word == "is", word_reps[i].is_stop_word)
            self.assertEqual(i == len(word_reps) - 1, word_reps[i].is_end_of_sentence)
            self.assertGreater(len(word_reps[i].replacements), 0)

    def test_should_replace(self):
        wr1 = WordRepresentation(word="I", is_stop_word=True, pos='s', replacements={"myself"})
        wr2 = WordRepresentation(word="hate", is_stop_word=False, pos='v', replacements={"loathe"})
        wr3 = WordRepresentation(word="South Bend", is_stop_word=False, pos='n', replacements={"horrorville"})
        wr4 = WordRepresentation(word="alot", is_stop_word=False, pos='r', replacements=set())
        word_representations = [wr1, wr2, wr3, wr4]
        expected_return_val = [False, True, False, False]
        for i, wr in enumerate(word_representations):
            self.assertEqual(SimpleWordReplacementStep._should_replace(wr), expected_return_val[i])

    def get_word_replacement_step(self, replacement_rate=0.15):
        return SimpleWordReplacementStep(1, replacement_rate)

    def word_replacement_test(self, orig_content, indices2sample, replacement_rate):
        step = self.get_word_replacement_step(replacement_rate)
        new_content = step._augment_content(orig_content)
        orig_words = orig_content.split()
        n_replacements = 0
        for i, word in enumerate(new_content.split()):
            if word != orig_words[i]:
                self.assertIn(i, indices2sample)
                n_replacements += 1
        self.assertEqual(n_replacements, min(math.ceil(len(orig_words) * replacement_rate), len(indices2sample)))
