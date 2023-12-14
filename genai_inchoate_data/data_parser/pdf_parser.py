import os
import fitz
import time
import uuid
import copy
import pypdf
import hashlib
from pathlib import Path
from genai_inchoate_data.data_parser.data_parser import DataParser


class PDFParser(DataParser):
    def __init__(self, pdf_path):
        self.pdf_path = Path(pdf_path)

    def extract_metadata(self):
        return "Extract metadata not implemented..!"
    
    def get_document_id(self):
        return f'{uuid.uuid4()}'

    def extract_text(self):
        docs = {}
        with open(self.pdf_path, "rb") as fp:
            pdf = pypdf.PdfReader(fp)
            num_pages = len(pdf.pages)
            for page in range(num_pages):
                docs[page+1] = pdf.pages[page].extract_text()
            return docs

    def extract_images(self, output_folder):
        pass

    def extract_tables(self):
        # Implement table extraction logic using PyMuPDF
        # (Note: PyMuPDF is more focused on text extraction, so table extraction might be less straightforward)
        return ["Table 1", "Table 2"]
