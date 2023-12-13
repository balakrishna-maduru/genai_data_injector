import os
import unittest
from genai_inchoate_data.utilities.file_reader import FileReader

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.yaml_file_path = 'test.yaml'
        self.json_file_path = 'test.json'
        self.csv_file_path = 'test.csv'

        # Create test files
        with open(self.yaml_file_path, 'w') as file:
            file.write("key: value")

        with open(self.json_file_path, 'w') as file:
            file.write('{"key": "value"}')

        with open(self.csv_file_path, 'w') as file:
            file.write("name,age\nJohn,30\nJane,25")

    def tearDown(self):
        # Clean up test files
        file_paths = [self.yaml_file_path, self.json_file_path, self.csv_file_path]
        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_read_yaml(self):
        reader = FileReader(self.yaml_file_path)
        data = reader.read_file()
        self.assertEqual(data, {'key': 'value'})

    def test_read_json(self):
        reader = FileReader(self.json_file_path)
        data = reader.read_file()
        self.assertEqual(data, {'key': 'value'})

    def test_read_csv(self):
        reader = FileReader(self.csv_file_path)
        data = reader.read_file()
        expected_data = [{'name': 'John', 'age': '30'}, {'name': 'Jane', 'age': '25'}]
        self.assertEqual(data, expected_data)

    def test_unsupported_format(self):
        reader = FileReader('test.txt')
        with self.assertRaises(ValueError):
            reader.read_file()

if __name__ == '__main__':
    unittest.main()
