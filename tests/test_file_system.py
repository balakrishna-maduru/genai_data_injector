import unittest
from unittest.mock import MagicMock
from genai_inchoate_data.utilities.file_system import FileSystem

class TestFileSystem(unittest.TestCase):
    def setUp(self):
        # Mock the fsspec filesystem for testing
        self.mock_source_fs = MagicMock()
        self.mock_destination_fs = MagicMock()

        # Initialize the FileSystem instance with mocked filesystems
        self.file_system = FileSystem(self.mock_source_fs, self.mock_destination_fs)

    def test_copy(self):
        # Define your test paths
        from_path = 'source.txt'
        to_path = 'destination.txt'

        # Mock the open and read methods of the source filesystem
        self.mock_source_fs.open.return_value.__enter__.return_value.read.return_value = b'Test content'

        # Perform the copy operation
        self.file_system.copy(from_path, to_path)

        # Assert that the destination filesystem's open and write methods were called
        self.mock_destination_fs.open.assert_called_once_with(to_path, 'wb')
        self.mock_destination_fs.open.return_value.__enter__.return_value.write.assert_called_once_with(b'Test content')

    def test_move(self):
        from_path = 'source.txt'
        to_path = 'destination.txt'

        # Mock the copy and rm methods
        self.file_system.copy = MagicMock()
        self.file_system.rm = MagicMock()

        # Perform the move operation
        self.file_system.move(from_path, to_path)

        # Assert that copy and rm were called with the correct arguments
        self.file_system.copy.assert_called_once_with(from_path, to_path)
        self.file_system.rm.assert_called_once_with(from_path)

    def test_rm(self):
        file_path = 'file.txt'

        # Perform the rm operation
        self.file_system.rm(file_path)

        # Assert that the source filesystem's rm method was called
        self.mock_source_fs.rm.assert_called_once_with(file_path)
    
if __name__ == '__main__':
    unittest.main()
