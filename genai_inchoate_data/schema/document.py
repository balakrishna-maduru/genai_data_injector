from enum import Enum, auto
from dataclasses import dataclass, Field
from typing import Optional, List, Dict


class MetadataMode(str, Enum):
    ALL = auto()
    EMBED = auto()
    LLM = auto()
    NONE = auto()



metadata_keys = [
      "file_name",
      "file_type",
      "file_size",
      "creation_date",
      "last_modified_date",
      "last_accessed_date"
    ]

@dataclass
class Metadata:
    file_path: str
    file_name: str
    file_type: str
    file_size: int
    creation_date: str
    last_modified_date: str
    last_accessed_date: Optional[str] = None
    page_label: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)

@dataclass
class RelatedNodeInfo:
    node_id: Optional[str] = None
    node_type: Optional[str] = None
    metadata: Optional[Metadata] = None
    hash: Optional[str] = None
    class_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        metadata_dict = data_dict.get('metadata', {})
        if all(key in metadata_dict for key in ['file_path', 'file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date']):
            metadata_instance = Metadata.from_dict(metadata_dict)
        else:
            metadata_instance = Metadata(file_path="", file_name="", file_type="", file_size=0, creation_date="", last_modified_date="")
        return cls(node_id=data_dict['node_id'], node_type=data_dict['node_type'], metadata=metadata_instance, hash=data_dict['hash'], class_name=data_dict['class_name'])
    
@dataclass
class Relationships:
    relationship_info: Dict[str, RelatedNodeInfo]

    @classmethod
    def from_dict(cls, data_dict):
        relationship_info_dict = data_dict.get('relationship_info', {})
        if not relationship_info_dict:
            return cls(relationship_info={})
        
        return cls({key: RelatedNodeInfo.from_dict(value) for key, value in relationship_info_dict.items()})

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
    metadata_separator: Optional[str] = "\n"
    class_name: Optional[str] = None
    load_details: Optional[LoadDetails] = None

    @classmethod
    def from_dict(cls, data_dict):
        metadata_dict = data_dict.get('metadata', {})  # Use get to avoid KeyError
        data_dict['metadata'] = Metadata.from_dict(metadata_dict)
        
        relationships_dict = data_dict.get('relationships', {})
        data_dict['relationships'] = Relationships.from_dict(relationships_dict)
        
        load_details_dict = data_dict.get('load_details', {})
        data_dict['load_details'] = LoadDetails.from_dict(load_details_dict)
        
        return cls(**data_dict)
    
    def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
        """Get object content."""
        metadata_str = self.get_metadata_str(mode=metadata_mode).strip()
        if not metadata_str:
            return self.text

        return self.text_template.format(
            content=self.text, metadata_str=metadata_str
        ).strip()

    def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
        """Metadata info string."""
        if mode == MetadataMode.NONE:
            return ""

        usable_metadata_keys = list(self.metadata.__dict__.keys())
        if mode == MetadataMode.LLM:
            if self.excluded_llm_metadata_keys: # type: ignore
                for key in self.excluded_llm_metadata_keys: # type: ignore
                    if key in usable_metadata_keys:
                        usable_metadata_keys.remove(key)
        elif mode == MetadataMode.EMBED:
            if self.excluded_embed_metadata_keys:
                for key in self.excluded_embed_metadata_keys: # type: ignore
                    if key in usable_metadata_keys:
                        usable_metadata_keys.remove(key)

        return '\n'.join(
            [
                '{key}:{value}'.format(key=key, value=str(value))  # type: ignore
                for key, value in self.metadata.__dict__.items() # type: ignore
                if key in usable_metadata_keys
            ]
        )


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
