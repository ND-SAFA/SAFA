import math

from test.base_test import BaseTest
from tracer.datasets.data_augmenter import DataAugmenter, WordRepresentation
from nltk.corpus import wordnet as wn


class TestDataAugmenter(BaseTest):

    def test_run(self):
        da = self.get_data_augmenter()
        data_entries = ["0The city planning is missing in this depressing city", "1the cars always break",
                        "2I hate South Bend alot", "3South Bend is frigid"]
        result = list(da.run(data_entries, 7))
        self.assertEquals(len(result), 7-len(data_entries))
        for augmented_data, i in result:
            self.assertEquals(int(data_entries[i][0]), i)

    def test_get_number_to_sample(self):
        self.assertEquals(2, DataAugmenter._get_number_to_sample(5, 5, 12))
        self.assertEquals(0, DataAugmenter._get_number_to_sample(5, 5, 10))
        self.assertEquals(5, DataAugmenter._get_number_to_sample(5, 5, 17))

    def test_generate_new_content(self):
        orig_content = "The city planning is missing in this depressing city and the cars always break"
        indices2sample = [4, 7, 12, 13]

        new_content = DataAugmenter._generate_new_content(orig_content, 0.15)
        self.word_replacement_test(orig_content, new_content, indices2sample, 0.15)

        new_content = DataAugmenter._generate_new_content(orig_content, 0.3)
        self.word_replacement_test(orig_content, new_content, indices2sample, 0.3)

    def test_get_synonyms(self):
        synonyms = {syn.lower() for syn in DataAugmenter._get_synonyms("south", "n")}
        self.assertTrue("south" not in synonyms)
        self.assertTrue("southward" in synonyms)

    def test_get_word_pos(self):
        noun = DataAugmenter._get_word_pos("NNP")
        self.assertEquals(wn.NOUN, noun)
        verb = DataAugmenter._get_word_pos("VBZ")
        self.assertEquals(wn.VERB, verb)
        adj = DataAugmenter._get_word_pos("JJ")
        self.assertEquals(wn.ADJ, adj)
        adv = DataAugmenter._get_word_pos("RB")
        self.assertEquals(wn.ADV, adv)
        unk = DataAugmenter._get_word_pos("PDT")
        self.assertEquals(None, unk)

    def test_to_word_representation(self):
        orig_content = "South Bend is frigid"
        orig_words = orig_content.split()
        word_reps = DataAugmenter._to_word_representations(orig_content)
        self.assertEquals(len(orig_words), len(word_reps))
        for i, word in enumerate(orig_words):
            self.assertEquals(word, word_reps[i].word)
            self.assertEquals(word == "is", word_reps[i].is_stop_word)
            self.assertEquals(i == len(word_reps) - 1, word_reps[i].is_end_of_sentence)
            self.assertGreater(len(word_reps[i].replacements), 0)

    def test_should_replace(self):
        wr1 = WordRepresentation(word="I", is_stop_word=True, pos='s', replacements={"myself"})
        wr2 = WordRepresentation(word="hate", is_stop_word=False, pos='v', replacements={"loathe"})
        wr3 = WordRepresentation(word="South Bend", is_stop_word=False, pos='n', replacements={"horrorville"})
        wr4 = WordRepresentation(word="alot", is_stop_word=False, pos='r', replacements=set())
        word_representations = [wr1, wr2, wr3, wr4]
        expected_return_val = [False, True, False, False]
        for i, wr in enumerate(word_representations):
            self.assertEquals(DataAugmenter._should_replace(wr), expected_return_val[i])

    def get_data_augmenter(self):
        return DataAugmenter(0.15)

    def word_replacement_test(self, orig_content, new_content, indices2sample, replacement_rate):
        orig_words = orig_content.split()
        n_replacements = 0
        for i, word in enumerate(new_content.split()):
            if word != orig_words[i]:
                self.assertIn(i, indices2sample)
                n_replacements += 1
        self.assertEquals(n_replacements, min(math.ceil(len(orig_words) * replacement_rate), len(indices2sample)))
