import os
from genai_inchoate_data.data_parser.data_parser import DataParser


class ExcelParser(DataParser):

    def __init__(self, excel_path):
        self.excel_path = excel_path

    def extract_metadata(self):
        metadata = {}
        metadata['file_name'] = os.path.basename(self.excel_path)
        metadata['file_location'] = os.path.dirname(os.path.abspath(self.excel_path))
        # Add more metadata extraction based on your Excel file structure
        return metadata

    def extract_text(self):
        # Excel files don't have direct text content, add implementation based on your needs
        pass

    def extract_images(self, output_folder):
        # Excel files may have embedded images, add implementation based on your needs
        pass

    def extract_tables(self):
        # Excel files may have embedded images, add implementation based on your needs
        pass
