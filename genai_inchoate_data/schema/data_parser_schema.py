from pydantic import BaseModel
from typing import List, Dict, Any

class Metadata(BaseModel):
    page_label: str
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    creation_date: str
    last_modified_date: str
    last_accessed_date: str

class Document(BaseModel):
    id_: str
    _embedding: Any = None
    _metadata: Metadata
    _hash: str
    _text: str
    _text_template: str
    _metadata_template: str
    _metadata_separator: str
    _class_name: str
