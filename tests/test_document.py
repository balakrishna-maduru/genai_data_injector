import unittest
from genai_inchoate_data.schema.document import Document, Data, Metadata, RelatedNodeInfo, Relationships, LoadDetails

class TestDocument(unittest.TestCase):

    def setUp(self):
        # Define a sample JSON data for testing
        self.sample_json_data = {
            "_id": "ee332da0-92ee-43b4-9370-559aaafc1268",
            "__data__": {
                "_id": "ee332da0-92ee-43b4-9370-559aaafc1268",
                "embedding": None,
                "metadata": {
                    "file_path": "/path/to/file",
                    "file_name": "example.txt",
                    "file_type": "text/plain",
                    "file_size": 1024,
                    "creation_date": "2023-01-01",
                    "last_modified_date": "2023-01-01",
                    "last_accessed_date": "2023-01-01"
                },
                "excluded_embed_metadata_keys": ["file_name"],
                "excluded_llm_metadata_keys": ["file_size"],
                "relationships": {
                    "1": {
                        "node_id": "node_id_1",
                        "node_type": "type_1",
                        "metadata": {
                            "file_path": "/path/to/related/file",
                            "file_name": "related.txt",
                            "file_type": "text/plain",
                            "file_size": 512,
                            "creation_date": "2023-01-01",
                            "last_modified_date": "2023-01-01",
                            "last_accessed_date": "2023-01-01"
                        },
                        "hash": "hash_1",
                        "class_name": "RelatedNodeInfo"
                    }
                },
                "hash": "data_hash",
                "text": "Sample text",
                "start_char_idx": None,
                "end_char_idx": None,
                "text_template": "{metadata_str}\n\n{content}",
                "metadata_template": "{key}: {value}",
                "metadata_separator": "\n",
                "class_name": "TextNode",
                "load_details": {
                    "date": "2023-01-01",
                    "time": 123456789.0,
                    "type_of_load": "initial"
                }
            },
            "__type__": "type_1"
        }

    def test_document_instance_creation(self):
        document_instance = Document.from_dict(self.sample_json_data)
        self.assertIsInstance(document_instance, Document)

    def test_document_id(self):
        document_instance = Document.from_dict(self.sample_json_data)
        self.assertEqual(document_instance._id, "ee332da0-92ee-43b4-9370-559aaafc1268")

    def test_document_data_instance(self):
        document_instance = Document.from_dict(self.sample_json_data)
        self.assertIsInstance(document_instance.__data__, Data)

    def test_document_metadata_instance(self):
        document_instance = Document.from_dict(self.sample_json_data)
        self.assertIsInstance(document_instance.__data__.metadata, Metadata)

    def test_document_relationships_instance(self):
        document_instance = Document.from_dict(self.sample_json_data)
        self.assertIsInstance(document_instance.__data__.relationships, Relationships)

    def test_document_load_details_instance(self):
        document_instance = Document.from_dict(self.sample_json_data)
        self.assertIsInstance(document_instance.__data__.load_details, LoadDetails)

    def test_document_metadata_attributes(self):
        document_instance = Document.from_dict(self.sample_json_data)
        metadata_instance = document_instance.__data__.metadata
        self.assertEqual(metadata_instance.file_path, "/path/to/file")   # type: ignore
        self.assertEqual(metadata_instance.file_name, "example.txt")  # type: ignore
        self.assertEqual(metadata_instance.file_type, "text/plain")  # type: ignore
        self.assertEqual(metadata_instance.file_size, 1024)  # type: ignore
        self.assertEqual(metadata_instance.creation_date, "2023-01-01")  # type: ignore
        self.assertEqual(metadata_instance.last_modified_date, "2023-01-01")  # type: ignore
        self.assertEqual(metadata_instance.last_accessed_date, "2023-01-01")  # type: ignore

    def test_document_relationship_info_attributes(self):
        document_instance = Document.from_dict(self.sample_json_data)
        relationship_info_instance = document_instance.__data__.relationships.relationship_info['1']  # type: ignore
        self.assertEqual(relationship_info_instance.node_id, "node_id_1")
        self.assertEqual(relationship_info_instance.node_type, "type_1")
        self.assertEqual(relationship_info_instance.hash, "hash_1")
        self.assertEqual(relationship_info_instance.class_name, "RelatedNodeInfo")

    def test_document_load_details_attributes(self):
        document_instance = Document.from_dict(self.sample_json_data)
        load_details_instance = document_instance.__data__.load_details
        self.assertEqual(load_details_instance.date, "2023-01-01")  # type: ignore
        self.assertEqual(load_details_instance.time, 123456789.0)  # type: ignore
        self.assertEqual(load_details_instance.type_of_load, "initial")  # type: ignore

if __name__ == '__main__':
    unittest.main()
