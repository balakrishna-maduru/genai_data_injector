from pymongo import MongoClient
from genai_inchoate_data.data_store.base_store import StoreInterface


class MongoDB(StoreInterface):
    def __init__(self, database_url, database_name):
        if isinstance(database_url, str):
            self.client = MongoClient(database_url)
        else:
            self.client = database_url
        self.db = self.client[database_name]

    def insert_document(self, collection_name, document):
        """
        Insert a document into the specified collection.

        Parameters:
        - collection_name (str): The name of the MongoDB collection.
        - document (dict): The document to be inserted.

        Returns:
        - str: The ObjectId of the inserted document.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)

    def find_document(self, collection_name, query):
        """
        Find documents in the specified collection based on the query.

        Parameters:
        - collection_name (str): The name of the MongoDB collection.
        - query (dict): The query to filter documents.

        Returns:
        - list: A list of documents matching the query.
        """
        collection = self.db[collection_name]
        cursor = collection.find(query)
        return list(cursor)

    def update_document(self, collection_name, query, update):
        """
        Update documents in the specified collection based on the query.

        Parameters:
        - collection_name (str): The name of the MongoDB collection.
        - query (dict): The query to filter documents.
        - update (dict): The update to be applied to matching documents.

        Returns:
        - int: The number of documents updated.
        """
        collection = self.db[collection_name]
        result = collection.update_many(query, {'$set': update})
        return result.modified_count

    def delete_document(self, collection_name, query):
        """
        Delete documents from the specified collection based on the query.

        Parameters:
        - collection_name (str): The name of the MongoDB collection.
        - query (dict): The query to filter documents.

        Returns:
        - int: The number of documents deleted.
        """
        collection = self.db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count
