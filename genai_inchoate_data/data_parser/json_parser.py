import os
import json
from genai_inchoate_data.data_parser.data_parser import DataParser


class JSONParser(DataParser):
    
    def __init__(self, json_path):
        self.json_path = json_path

    def extract_metadata(self):
        metadata = self.load_json()
        return metadata

    def extract_text(self):
        text = self.load_json()
        # Add more text extraction based on your JSON structure
        return text

    def extract_images(self, output_folder):
        # Add implementation for extracting images from JSON data
        pass

    def extract_tables(self):
        # Add implementation for extracting tables from JSON data
        pass

    def load_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
