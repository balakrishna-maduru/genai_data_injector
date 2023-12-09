import os
import fitz
from genai_inchoate_data.data_parser.data_parser import DataParser


class PDFParser(DataParser):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_metadata(self):
        with fitz.open(self.pdf_path) as pdf_document:
            metadata = pdf_document.metadata
        return metadata

    def extract_text(self):
        with fitz.open(self.pdf_path) as pdf_document:
            text = ''
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()
        return text

    def extract_images(self, output_folder):
        with fitz.open(self.pdf_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                images = page.get_images(full=True)
                for img_index, img_info in enumerate(images):
                    image_index, base_image = img_info
                    image_bytes = base_image.get_data()
                    # Save image to the output folder
                    with open(os.path.join(output_folder, f"image_{page_number}_{img_index}.png"), 'wb') as img_file:
                        img_file.write(image_bytes)


    def extract_tables(self):
        # Implement table extraction logic using PyMuPDF
        # (Note: PyMuPDF is more focused on text extraction, so table extraction might be less straightforward)
        return ["Table 1", "Table 2"]
