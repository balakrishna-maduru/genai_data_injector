from genai_inchoate_data.data_store.mongo_db import MongoDB

class Store:
    def __init__(self):
        self.factory_map = {
            'mongo_db': MongoDB
        }

    def get(self, store):
        factory_class = self.factory_map.get(store.type)
        if factory_class:
            return factory_class(store.db_url, store.db_name) # type: ignore
        else:
            raise ValueError(f"Unsupported database type: {store.type}")
