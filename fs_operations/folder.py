# folder.py
from fs_operations.file_reader import FileReader
from fs_operations.extension_mapper import ExtensionMapper
from fs_operations.file_system import FileSystem, get_file_system

class Folder:
    def __init__(self, file_system=None, extension_mapper=None,filesystem_type='file', **kwargs):
        self.children = [] 
        self.extension_mapper = extension_mapper or ExtensionMapper() 
        self.file_system = file_system or FileSystem(get_file_system(filesystem_type, **kwargs))
        self.results = {}

    def add(self, component):
        self.children.append(component)

    def add_file(self, file_path):
        _, extension = file_path.rsplit('.', 1)

        # Get the appropriate reader class based on the file extension
        reader_class = self.extension_mapper.get_reader_class(extension, self.file_system)
        reader = reader_class(file_path, self.file_system)
        self.add(reader)

    def read(self):
        for child in self.children:
            if isinstance(child, FileReader):
                file_name = getattr(child, 'file_path', 'UnknownFile')
                self.results[file_name] = child.read()
            elif isinstance(child, Folder):
                child.read()
