from abc import ABC, abstractmethod

class DataParser(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def extract_metadata(self):
        return "Extract metadata not implemented..!"

    @abstractmethod
    def extract_text(self):
        return "Extract text not implemented..!"

    @abstractmethod
    def extract_images(self, output_folder):
        return "Extract images not implemented..!"

    @abstractmethod
    def extract_tables(self):
        return "Extract table not implemented..!"


class DefaultParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = self.extract_metadata()

    @abstractmethod
    def extract_metadata(self):
        return "Extract metadata not implemented..!"

    @abstractmethod
    def extract_text(self):
        return "Extract text not implemented..!"

    @abstractmethod
    def extract_images(self, output_folder):
        return "Extract images not implemented..!"

    @abstractmethod
    def extract_tables(self):
        return "Extract table not implemented..!"