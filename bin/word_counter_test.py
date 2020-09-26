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


if __name__ == "__main__":
    unittest.main()
