# image_file_reader.py
from fs_operations.file_reader import FileReader
from PIL import Image
from io import BytesIO

class ImageFileReader(FileReader):
    supported_extensions = ['jpg', 'jpeg', 'png', 'gif']

    def __init__(self, file_path, file_system):
        super().__init__(file_path, file_system)
        self.file_system = file_system

    def read(self):
        try:
            image_bytes = self.file_system.read(self.file_path, binary=True)
            with BytesIO(image_bytes) as image_buffer:
                image = Image.open(image_buffer)
                return list(image.getdata())
        except FileNotFoundError:
            return f"Image file not found: {self.file_path}"
