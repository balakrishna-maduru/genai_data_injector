from pdf_parser import  PDFParser
from json_parser import JSONParser
from text_parser import TextParser
from image_parser import ImageParser
from word_parser import WordParser
from excel_parser import ExcelParser

class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.factory_map = {
            'pdf': PDFParser,
            'json': JSONParser,
            'txt': TextParser,
            'png': ImageParser,
            'jpg': ImageParser,
            'docx': WordParser,
            'xlsx': ExcelParser,
        }

    def create_parser(self):
        file_extension = self.get_file_extension()
        factory_class = self.factory_map.get(file_extension)
        if factory_class:
            return factory_class.create_parser(self.file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def get_file_extension(self):
        return self.file_path.split('.')[-1].lower()