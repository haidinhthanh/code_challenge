import unittest
from bin.word_counter import WordCounter
from os import path
from constant.path import TEST_PATH
import logging

#
# class WordCounterTest(unittest.TestCase):
#     def setUp(self):
#         self.word_counter = WordCounter(mode="test")
#
#     def test_is_frequency_is_true(self):
#         dictionary = self.word_counter.cal_word_frequency_in_doc(
#             document_path=path.join(TEST_PATH, "test_is_frequency_is_true"), arrange_type="desc"
#         )
#
#         self.assertEqual(dictionary["trump"], 30, "Text should have 30 word trump")
#         self.assertEqual(dictionary["giá"], 2, "Text should have 2 word giá")
#
#     def test_text_is_empty(self):
#         dictionary = self.word_counter.cal_word_frequency_in_doc(
#             document_path=path.join(TEST_PATH, "test_text_is_empty"), arrange_type="desc"
#         )
#         self.assertEqual(dictionary, {}, "Class should return empty dict")
#
#     def test_punctuation_mark_not_in_freq_dict(self):
#         dictionary = self.word_counter.cal_word_frequency_in_doc(
#             document_path=path.join(TEST_PATH, "test_is_frequency_is_true"), arrange_type="desc"
#         )
#         self.assertEqual("!" in dictionary.keys(), False, "Dict should not have punctuation mark")
#
#     def test_file_text_not_exist(self):
#         self.assertRaises(FileNotFoundError, self.word_counter.cal_word_frequency_in_doc,
#                           path.join(TEST_PATH, "fake"))
#
#
# if __name__ == "__main__":
#     # unittest.main()
#     suite = unittest.TestLoader().loadTestsFromTestCase(WordCounterTest)
#     unittest.TextTestRunner(verbosity=2).run(suite)



print(path.join(TEST_PATH, "test_is_frequency_is_true"))