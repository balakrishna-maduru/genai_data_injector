from genai_inchoate_data.data_parser.pdf_parser import  PDFParser
from genai_inchoate_data.data_parser.json_parser import JSONParser
from genai_inchoate_data.data_parser.text_parser import TextParser
from genai_inchoate_data.data_parser.image_parser import ImageParser
from genai_inchoate_data.data_parser.word_parser import WordParser
from genai_inchoate_data.data_parser.excel_parser import ExcelParser

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

    def extract_text(self):
        file_extension = self.get_file_extension()
        factory_class = self.factory_map.get(file_extension)
        if factory_class:
            return factory_class(self.file_path).extract_text()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def get_file_extension(self):
        return self.file_path.split('.')[-1].lower()