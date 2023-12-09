import os
from genai_inchoate_data.data_parser.data_parser import DataParser


class TextParser(DataParser):
    def __init__(self, text_path):
        self.text_path = text_path

    def extract_metadata(self):
        metadata = {}
        metadata['file_name'] = os.path.basename(self.text_path)
        metadata['file_location'] = os.path.dirname(os.path.abspath(self.text_path))
        # Add more metadata extraction based on your text file structure
        return metadata

    def extract_text(self):
        with open(self.text_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    def extract_images(self, output_folder):
        # Text files don't have images, so this method is left empty
        pass

    def extract_tables(self):
        # Text files don't have tables, so this method is left empty
        pass
