from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class Metadata:
    file_path: str
    file_name: str
    file_type: str
    file_size: int
    creation_date: str
    last_modified_date: str
    last_accessed_date: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

@dataclass
class RelatedNodeInfo:
    node_id: str
    node_type: str
    metadata: Metadata
    hash: str
    class_name: str

    @classmethod
    def from_dict(cls, data_dict):
        data_dict['metadata'] = Metadata.from_dict(data_dict['metadata'])
        return cls(**data_dict)

@dataclass
class Relationships:
    relationship_info: Dict[str, RelatedNodeInfo]

    @classmethod
    def from_dict(cls, data_dict):
        return cls({key: RelatedNodeInfo.from_dict(value) for key, value in data_dict.items()})

@dataclass
class LoadDetails:
    date: str
    time: float
    type_of_load: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

@dataclass
class Data:
    _id: Optional[str] = None
    doc_id: Optional[str] = None
    embedding: Optional[None] = None
    metadata: Optional[Metadata] = None
    excluded_embed_metadata_keys: Optional[List[str]] = None
    excluded_llm_metadata_keys: Optional[List[str]] = None
    relationships: Optional[Relationships] = None
    hash: Optional[str] = None
    text: Optional[str] = None
    start_char_idx: Optional[None] = None
    end_char_idx: Optional[None] = None
    text_template: Optional[str] = None
    metadata_template: Optional[str] = None
    metadata_separator: Optional[str] = None
    class_name: Optional[str] = None
    load_details: Optional[LoadDetails] = None

    @classmethod
    def from_dict(cls, data_dict):
        data_dict['metadata'] = Metadata.from_dict(data_dict.get('metadata', {}))
        relationships_dict = data_dict.get('relationships', {})
        data_dict['relationships'] = Relationships.from_dict(relationships_dict)
        data_dict['load_details'] = LoadDetails.from_dict(data_dict.get('load_details', {}))
        return cls(**data_dict)

@dataclass
class Document:
    _id: str
    __data__: Data
    __type__: str

    @classmethod
    def from_dict(cls, data_dict):
        data_dict['__data__'] = Data.from_dict(data_dict['__data__'])
        return cls(**data_dict)



import json
# with open("/Users/balakrishnamaduru/Documents/git/genai_data_injector/notebooks/storage/docstore.json") as file:
#     data_dict = json.load(file)['docstore/data']['7f44d9cd-188f-4aec-bf05-338c0644f695']

# # Create an instance of Document
# your_json_data_instance = Document.from_dict(data_dict)

# # Access the data
# print(your_json_data_instance.__data__.id_)
# print(your_json_data_instance.__data__.metadata.file_path)
# print(your_json_data_instance.__data__.relationships.relationship_info['1'].node_id)
