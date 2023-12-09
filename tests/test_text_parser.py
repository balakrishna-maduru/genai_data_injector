import os
import unittest
from . import resource_path
from genai_inchoate_data.data_parser.text_parser import TextParser

class TestTextParser(unittest.TestCase):
    def setUp(self):
        self.text_path = os.path.join(resource_path, 'input/sample.txt')
        self.output_path = os.path.join(resource_path, 'output')
        self.parser = TextParser(self.text_path)

    def test_extract_metadata(self):
        metadata = self.parser.extract_metadata()
        self.assertIsNotNone(metadata)
        # Add more specific assertions based on your expectations

    def test_extract_text(self):
        text = self.parser.extract_text()
        self.assertIsNotNone(text)
        # Add more specific assertions based on your expectations

    def test_extract_images(self):
        self.parser.extract_images(self.output_path)
        # Add assertions to check if images are extracted to the output folder

    def test_extract_tables(self):
        tables = self.parser.extract_tables()
        # No tables in text files, add more specific assertions based on your expectations

if __name__ == '__main__':
    unittest.main()
