import os
import unittest
from pymongo import MongoClient
from mongomock import MongoClient as MockMongoClient
from genai_inchoate_data.data_store.mongo_db import MongoDB 

class TestMongoDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use mongomock for testing instead of a real MongoDB server
        cls.client = MockMongoClient()
        cls.test_db = cls.client['test_database']
        cls.interface = MongoDB(cls.client, 'test_database')

    def setUp(self):
        # Create a test collection for each test case
        self.test_collection = self.test_db[self.id()]

    def tearDown(self):
        # Drop the test collection after each test case
        self.test_db.drop_collection(self.id())

    def test_insert_document(self):
        document_id = self.interface.insert_document(self.id(), {'key': 'value'})
        self.assertIsNotNone(document_id)

    def test_find_document(self):
        # Insert a document for testing
        self.interface.insert_document(self.id(), {'key': 'value'})

        # Find the inserted document
        query = {'key': 'value'}
        documents = self.interface.find_document(self.id(), query)
        self.assertEqual(len(documents), 1)

    def test_update_document(self):
        # Insert a document for testing
        document_id = self.interface.insert_document(self.id(), {'key': 'value'})

        # Update the inserted document
        query = {'_id': document_id}
        update = {'key': 'new_value'}
        num_updated = self.interface.update_document(self.id(), query, update)
        self.assertEqual(num_updated, 1)

        # Check that the document has been updated
        updated_document = self.interface.find_document(self.id(), query)
        self.assertEqual(updated_document[0]['key'], 'new_value')

    def test_delete_document(self):
        # Insert a document for testing
        document_id = self.interface.insert_document(self.id(), {'key': 'value'})

        # Delete the inserted document
        query = {'_id': document_id}
        num_deleted = self.interface.delete_document(self.id(), query)
        self.assertEqual(num_deleted, 1)

        # Check that the document has been deleted
        deleted_document = self.interface.find_document(self.id(), query)
        self.assertEqual(len(deleted_document), 0)

if __name__ == '__main__':
    unittest.main()
