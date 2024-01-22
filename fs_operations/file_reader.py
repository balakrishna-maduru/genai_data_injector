# file_reader.py

class FileReader:
    def __init__(self, file_path, file_system):
        self.file_path = file_path
        self.file_system = file_system

    def read(self):
        try:
            return self.file_system.read(self.file_path)
        except FileNotFoundError:
            return f"File not found: {self.file_path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
