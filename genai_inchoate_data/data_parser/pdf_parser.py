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
        self.metadata = self.extract_metadata()

    def extract_metadata(self):
        creation_time = os.path.getctime(self.pdf_path)
        modification_time = os.path.getmtime(self.pdf_path)
        return {
            "file_name": os.path.basename(self.pdf_path),
            "file_path": self.pdf_path.as_posix(),
            "file_size": os.path.getsize(self.pdf_path),
            "file_type": self.pdf_path.suffix,
            "creation_time": time.ctime(creation_time),
            "modification_time": time.ctime(modification_time)
        }

    def generate_hash(self, input_string):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode('utf-8'))
        hashed_string = sha256_hash.hexdigest()
        return hashed_string
    
    def get_document_id(self):
        return f'{uuid.uuid4()}'

    def extract_text(self):
        docs = []
        with open(self.pdf_path, "rb") as fp:
            pdf = pypdf.PdfReader(fp)
            num_pages = len(pdf.pages)
            docs = []
            for page in range(num_pages):
                page_text = pdf.pages[page].extract_text()
                self.metadata['page_label'] = page+1
                print(self.metadata)
                doc_id = self.get_document_id()
                docs.append({
                    "_id": doc_id,
                    "doc_id":doc_id,
                    "text":page_text,
                    "metadata":copy.deepcopy(self.metadata),
                    "hash":self.generate_hash(page_text)})
            return docs

    def extract_images(self, output_folder):
        pass

    def extract_tables(self):
        # Implement table extraction logic using PyMuPDF
        # (Note: PyMuPDF is more focused on text extraction, so table extraction might be less straightforward)
        return ["Table 1", "Table 2"]
