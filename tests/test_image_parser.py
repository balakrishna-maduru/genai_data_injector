import os
import unittest
from . import resource_path
from genai_inchoate_data.data_parser.image_parser import ImageParser

class TestImageParser(unittest.TestCase):
    def setUp(self):
        self.image_path = os.path.join(resource_path, 'input/sample.png')
        self.output_path = os.path.join(resource_path, 'output')
        self.parser = ImageParser(self.image_path)

    def test_extract_metadata(self):
        metadata = self.parser.extract_metadata()
        self.assertIsNotNone(metadata)
        # Add more specific assertions based on your expectations

    def test_extract_text(self):
        text = self.parser.extract_text()
        self.assertIsNone(text)
        # No text in image files, add more specific assertions based on your expectations

    def test_extract_images(self):
        self.parser.extract_images(self.output_path)
        # No images to extract in image files, add assertions based on your expectations

    def test_extract_tables(self):
        tables = self.parser.extract_tables()
        self.assertIsNone(tables)
        # No tables in image files, add more specific assertions based on your expectations

if __name__ == '__main__':
    unittest.main()
