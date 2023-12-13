import abc
class StoreInterface(abc.ABC):
      
      def __init__(self, database_url, database_name):
        pass

      @abc.abstractclassmethod
      def insert_document(self, collection_name, document):
        pass

      @abc.abstractclassmethod
      def find_document(self, collection_name, query):
        pass

      @abc.abstractclassmethod
      def update_document(self, collection_name, query, update):
        pass

      @abc.abstractclassmethod
      def delete_document(self, collection_name, query):
        pass