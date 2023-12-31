import uuid
import time
from datetime import datetime
from genai_inchoate_data.data_store.store import Store
from genai_inchoate_data.utilities.file_reader import FileReader
from genai_inchoate_data.utilities.configurations import Configurations
from genai_inchoate_data.utilities.file_system import FileSystem, get_file_system


class Loader:

    def __init__(self, config_file) -> None:
        self.config = config_file
        if not isinstance(self.config, dict):
            self.config = FileReader(config_file).read_file()
        self.config_details = Configurations(self.config)
        self.store = Store().get(self.config_details.store) # type: ignore

    def load_details(self):
        return {"date": datetime.now().strftime("%Y-%m-%d"),
                "time": time.time()
                }

    def load(self):
        source_fs = get_file_system(self.config_details.source_file_system) # type: ignore
        target_fs = get_file_system(self.config_details.target_file_system) # type: ignore
        fs = FileSystem(source_fs=source_fs, destination_fs=target_fs)
        fs.copy(self.config_details.source_location, self.config_details.target_location) # type: ignore
        if self.config_details.write_metadata: # type: ignore
            metadata = fs.info(self.config_details.source_location) # type: ignore
            data = { "_id": f'{uuid.uuid4()}',
                    "metadata": metadata,
                    "load_details": self.load_details()
                    }
            print(data)
            self.store.insert_document(self.config_details.store.collection_name,data)  # type: ignore
