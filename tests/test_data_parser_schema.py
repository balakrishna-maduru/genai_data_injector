import unittest
from genai_inchoate_data.schema.data_parser_schema import Document, Metadata

class TestDocument(unittest.TestCase):

    def setUp(self):
        # Example JSON data
        self.json_data = {
            "id_": "da592064-9e43-401e-823c-381218d4829b",
            "embedding": None,
            "metadata": {
                "page_label": "2",
                "file_name": "lyft_2021.pdf",
                "file_path": "lyft_2021.pdf",
                "file_type": "application/pdf",
                "file_size": 1440303,
                "creation_date": "2023-11-16",
                "last_modified_date": "2023-11-16",
                "last_accessed_date": "2023-11-16"
            },
            "excluded_embed_metadata_keys": [
                "file_name",
                "file_type",
                "file_size",
                "creation_date",
                "last_modified_date",
                "last_accessed_date"
            ],
            "excluded_llm_metadata_keys": [
                "file_name",
                "file_type",
                "file_size",
                "creation_date",
                "last_modified_date",
                "last_accessed_date"
            ],
            "relationships": {},
            "hash": "029bdf370c7335835ba696f1963b1b75aa6f892a37fbc77f4d171a12c18ab6a8",
            "text": "Table of ContentsPage ...",
            "text_template": "{metadata_str}{content}",
            "metadata_template": "{key}: {value}",
            "metadata_separator": "",
            "class_name": "Document"
        }

    def test_document_attributes(self):
        document_instance = Document(**self.json_data)
        print(f"document_instance {document_instance}")
        print(f"document_instance --> {dir(document_instance)}")

        self.assertEqual(document_instance.id_, "da592064-9e43-401e-823c-381218d4829b")
        self.assertEqual(document_instance.hash, "029bdf370c7335835ba696f1963b1b75aa6f892a37fbc77f4d171a12c18ab6a8")
        self.assertIsInstance(document_instance.metadata, Metadata)

    def test_metadata_attributes(self):
        document_instance = Document(**self.json_data)
        metadata_instance = document_instance.metadata

        self.assertEqual(metadata_instance.page_label, "2")
        self.assertEqual(metadata_instance.file_name, "lyft_2021.pdf")
        self.assertEqual(metadata_instance.file_type, "application/pdf")

    def test_text_template(self):
        document_instance = Document(**self.json_data)
        print(f"document_instance : ---> {document_instance}")
        expected_text_template = "id_='da592064-9e43-401e-823c-381218d4829b' embedding=None metadata=Metadata(page_label='2', file_name='lyft_2021.pdf', file_path='lyft_2021.pdf', file_type='application/pdf', file_size=1440303, creation_date='2023-11-16', last_modified_date='2023-11-16', last_accessed_date='2023-11-16') excluded_embed_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'] excluded_llm_metadata_keys=['file_name', 'file_type', 'file_size', 'creation_date', 'last_modified_date', 'last_accessed_date'] relationships={} hash='029bdf370c7335835ba696f1963b1b75aa6f892a37fbc77f4d171a12c18ab6a8' text='Table of ContentsPage ...' text_template='{metadata_str}{content}' metadata_template='{key}: {value}' metadata_separator='' class_name='Document'"
        self.assertEqual(str(document_instance), expected_text_template)

if __name__ == '__main__':
    unittest.main()
