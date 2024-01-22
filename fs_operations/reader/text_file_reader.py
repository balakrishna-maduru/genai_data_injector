import csv
import json
import yaml
from fs_operations.file_reader import FileReader

class TextFileReader(FileReader):
    supported_extensions = ['txt', 'text']

    def __init__(self, file_path, file_system):
        super().__init__(file_path, file_system)
        self.file_path = file_path
    
    def read(self):
        return self.file_system.read(self.file_path, binary=False)

class JsonFileReader(FileReader):
    supported_extensions = ['json']

    def __init__(self, file_path, file_system):
        super().__init__(file_path, file_system)
        self.file_path = file_path
    
    def read(self):
        return json.loads(self.file_system.read_text(self.file_path))

class YamlFileReader(FileReader):
    supported_extensions = ['yml', 'yaml']
    
    def __init__(self, file_path, file_system):
        super().__init__(file_path, file_system)
        self.file_path = file_path
    
    def read(self):
        return yaml.safe_load(self.file_system.read_text(self.file_path))

class CsvFileReader(FileReader):
    supported_extensions = ['csv']
    
    def __init__(self, file_path, file_system):
        super().__init__(file_path, file_system)
        self.file_path = file_path

    def read(self):
        reader = csv.DictReader(self.file_system.read_text(self.file_path))
        data = [row for row in reader]
        return data
