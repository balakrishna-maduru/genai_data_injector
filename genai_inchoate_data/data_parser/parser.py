import re
import copy
import hashlib
from pydoc import doc

from sqlalchemy import false
from genai_inchoate_data.data_parser.pdf_parser import  PDFParser
from genai_inchoate_data.data_parser.json_parser import JSONParser
from genai_inchoate_data.data_parser.text_parser import TextParser
from genai_inchoate_data.data_parser.image_parser import ImageParser
from genai_inchoate_data.data_parser.word_parser import WordParser
from genai_inchoate_data.data_parser.excel_parser import ExcelParser
from genai_inchoate_data.data_store.store import Store
from genai_inchoate_data.utilities.configurations import Configurations

class Parser:
    def __init__(self, store_config):
        if isinstance(store_config,dict):
            self.store_config = Configurations(store_config)
        self.factory_map = {
            'pdf': PDFParser,
            'json': JSONParser,
            'txt': TextParser,
            'png': ImageParser,
            'jpg': ImageParser,
            'docx': WordParser,
            'xlsx': ExcelParser,
        }
        self.store = Store().get(self.store_config)


    def get_documents(self, from_date=None, to_date=None, file_name_pattern=None, fetch_only_metadata=False):
        self.output_documents = []
        query = {}
        if from_date and to_date:
            query['load_details.date'] = {'$gte': from_date, '$lte': to_date}
        elif from_date:
            query['load_details.date'] = {'$gte': from_date}
        elif to_date:
            query['load_details.date'] = {'$lte': to_date}
        if file_name_pattern:
            query['metadata.file_name'] = {'$regex': re.compile(file_name_pattern)}
        
        if not query:
            documents = self.store.find_document(self.store_config.collection_name,query) # type: ignore
        else:
            documents = self.store.find_document(self.store_config.collection_name).limit(limit) # type: ignore
        if fetch_only_metadata:
            return documents
        self.extract_text_for_each_document(documents)
        return self.output_documents

    def extract_text_for_each_document(self, documents):
        for document in documents:
            self.iterate_documents(document)
    

    def iterate_documents(self, document):
        print(f'document : ${document}')
        temp_document = copy.deepcopy(document)
        docs = self.extract_text(document.get('metadata').get('name'))
        if isinstance(docs, dict):
            for page_number, text in docs.items():
                temp_document['_id'] = f'{document.get("_id")}#{page_number}'
                temp_document['metadata']['page_label'] = page_number
                self.add_text_and_hash(temp_document, text)
        else:
            self.add_text_and_hash(temp_document, docs)
    
    def add_text_and_hash(self, temp_document, text):
        temp_document['text'] = text
        temp_document['hash'] = self.generate_hash(text)
        self.output_documents.append(temp_document)

    def extract_text(self, file_name):
        file_extension = file_name.split('.')[-1].lower()
        factory_class = self.factory_map.get(file_extension)
        if factory_class:
            return factory_class(file_name).extract_text()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def generate_hash(self, input_string):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode('utf-8'))
        hashed_string = sha256_hash.hexdigest()
        return hashed_string
