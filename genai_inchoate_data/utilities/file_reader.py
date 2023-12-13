import yaml
import json
import csv

class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        file_extension = self.file_path.split('.')[-1].lower()

        if file_extension == 'yaml' or file_extension == 'yml':
            return self.read_yaml()
        elif file_extension == 'json':
            return self.read_json()
        elif file_extension == 'csv':
            return self.read_csv()
        else:
            raise ValueError("Unsupported file format")

    def read_yaml(self):
        with open(self.file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def read_json(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

    def read_csv(self):
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
