from fs_operations.file_reader import FileReader
import fitz

class PdfFileReader(FileReader):
    supported_extensions = ['pdf']

    def __init__(self, file_path, file_system):
        super().__init__(file_path, file_system)
        self.file_system = file_system

    def read(self):
        try:
            pdf_bytes = self.file_system.read(self.file_path, binary=True)
            pdf_document = fitz.open("pdf", pdf_bytes)
            num_pages = pdf_document.page_count
            page_texts = {}

            for page_num in range(num_pages):
                page = pdf_document[page_num]
                text_content = page.get_text()
                page_texts[page_num + 1] = text_content

            return page_texts
        except FileNotFoundError:
            return f"PDF file not found: {self.file_path}"
