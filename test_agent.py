import unittest
from tools import clean_text, count_words, reading_time
from agent import build_agent, State


class TestPipelineAgent(unittest.TestCase):
    def test_clean_text(self):
        sample = "Here is the outline:\n1. First\n2. Second\n3. Third"
        cleaned = clean_text(sample)
        self.assertEqual(cleaned, "1. First\n2. Second\n3. Third")

    def test_clean_text_normal(self):
        sample = "1. Point one\n2. Point two\n3. Point three"
        cleaned = clean_text(sample)
        self.assertEqual(cleaned, sample)

    def test_count_words(self):
        text = "This is a simple test sentence with nine words."
        self.assertEqual(count_words(text), 9)

    def test_reading_time(self):
        text = "word " * 100
        # 100 words / 200 wpm = 0.5 min = 30 sec
        self.assertEqual(reading_time(text), "30 sec")

    def test_graph_structure(self):
        graph = build_agent()
        self.assertIsNotNone(graph)


if __name__ == "__main__":
    unittest.main()
