import unittest
from bin.word_counter import WordCounter


class Test(unittest.TestCase):
    def setUp(self):
        print('setUp')
        self.word_counter = WordCounter()

    def test_is_frequency_is_true(self):
        dictionary = self.word_counter.cal_word_frequency_in_doc(
            document_path="../test_data/test_is_frequency_is_true", arrange_type="desc"
        )

        self.assertEqual(dictionary["trump"], 30, "Text should have 30 word trump")
        self.assertEqual(dictionary["giá"], 2, "Text should have 2 word giá")

    def test_text_is_empty(self):
        dictionary = self.word_counter.cal_word_frequency_in_doc(
            document_path="../test_data/test_text_is_empty", arrange_type="desc"
        )
        self.assertEqual(dictionary, {}, "Class should return empty dict")

    def test_punctuation_mark_not_in_freq_dict(self):
        dictionary = self.word_counter.cal_word_frequency_in_doc(
            document_path="../test_data/test_is_frequency_is_true", arrange_type="desc"
        )
        self.assertEqual("!" in dictionary.keys(), False, "Dict should not have punctuation mark")

    def test_file_text_not_exist(self):
        self.assertRaises(FileNotFoundError, self.word_counter.cal_word_frequency_in_doc,
                          "../test_data/fake")


if __name__ == "__main__":
    unittest.main()
