import os
import json
import importlib
from fs_operations.file_reader import FileReader
from fs_operations.reader.text_file_reader import TextFileReader
from fs_operations.reader.image_file_reader import ImageFileReader
from fs_operations.reader.pdf_file_reader import PdfFileReader




class ExtensionMapper:
    def __init__(self, mapping_path=f"{os.path.dirname(os.path.realpath(__file__))}/config/extension_mapping.json"):
        self.mapping = self.load_mapping(mapping_path)

    def dynamic_import(self):
        module = importlib.import_module('fs_operations.reader')
        my_class = getattr(module, 'MyClass')
        return my_class

    def load_mapping(self, mapping_path):
        with open(mapping_path, 'r') as json_file:
            return json.load(json_file)

    def get_reader_class(self, extension, file_system=None):
        reader_class_name = self.mapping.get(extension.lower(), "PdfFileReader")
        reader_class = globals().get(reader_class_name)
        return reader_class 
