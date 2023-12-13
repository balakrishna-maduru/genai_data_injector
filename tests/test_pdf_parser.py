import os
import unittest
from . import resource_path
from genai_inchoate_data.data_parser.pdf_parser import PDFParser

class TestPDFParser(unittest.TestCase):
    def setUp(self):
        self.pdf_path = os.path.join(resource_path, 'input/sample.pdf')
        self.output_path = os.path.join(resource_path, 'output')
        self.parser = PDFParser(self.pdf_path)

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
        self.assertIsNotNone(tables)
        # Add more specific assertions based on your expectations

if __name__ == '__main__':
    unittest.main()
