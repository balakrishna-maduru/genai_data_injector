import os
from genai_inchoate_data.data_parser.data_parser import DataParser


class ImageParser(DataParser):
    def __init__(self, image_path):
        self.image_path = image_path

    def extract_metadata(self):
        metadata = {}
        metadata['file_name'] = os.path.basename(self.image_path)
        metadata['file_location'] = os.path.dirname(os.path.abspath(self.image_path))
        # Add more metadata extraction based on your image file structure
        return metadata

    def extract_text(self):
        # Image files don't have text, so this method is left empty
        pass

    def extract_images(self, output_folder):
        # Image files don't have images (they are images), so this method is left empty
        pass

    def extract_tables(self):
        # Excel files may have embedded images, add implementation based on your needs
        pass
