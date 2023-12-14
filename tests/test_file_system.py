import os
import tempfile
import shutil
import unittest
from fsspec.implementations.local import LocalFileSystem
from genai_inchoate_data.utilities.file_system import FileSystem

class TestFileSystem(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create a real local filesystem for testing
        self.local_fs = LocalFileSystem()

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_makedirs(self):
        # Test creating directories recursively
        parent_directory = os.path.join(self.test_dir, 'parent')
        subdirectory = 'child_directory'

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Perform the makedirs operation
        fs.makedirs(os.path.join(parent_directory, subdirectory), exist_ok=True)

        # Check if the directories are created successfully
        self.assertTrue(os.path.exists(os.path.join(parent_directory, subdirectory)))
        self.assertTrue(os.path.isdir(os.path.join(parent_directory, subdirectory)))

    def test_walk(self):
        # Test walking through directories
        base_directory = os.path.join(self.test_dir, 'walk_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some nested directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Perform the walk operation
        walk_result = fs.walk(base_directory)

        # Check if the result contains the expected directories and files
        expected_walk_result = [
            (base_directory, ['dir1'], ['file1.txt']),
            (os.path.join(base_directory, 'dir1'), ['subdir'], []),
            (os.path.join(base_directory, 'dir1', 'subdir'), [], [])
        ]

        for actual, expected in zip(walk_result, expected_walk_result):
            self.assertEqual(actual[0], expected[0])
            self.assertEqual(sorted(actual[1]), sorted(expected[1]))
            self.assertEqual(sorted(actual[2]), sorted(expected[2]))

    def test_find(self):
        # Test finding files and directories
        base_directory = os.path.join(self.test_dir, 'find_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Perform the find operation
        find_result = fs.find(base_directory, withdirs=True, detail=True)

        # Check if the result contains the expected files and directories
        expected_find_result = [
            {'name': base_directory, 'type': 'directory', 'size': 0},
            {'name': os.path.join(base_directory, 'dir1'), 'type': 'directory', 'size': 0},
            {'name': os.path.join(base_directory, 'dir1', 'subdir'), 'type': 'directory', 'size': 0},
            {'name': os.path.join(base_directory, 'file1.txt'), 'type': 'file', 'size': os.path.getsize(os.path.join(base_directory, 'file1.txt'))}
        ]

        for actual, expected in zip(find_result, expected_find_result):
            self.assertEqual(actual['name'], expected['name'])
            self.assertEqual(actual['type'], expected['type'])
            self.assertEqual(actual['size'], expected['size'])

    def test_du(self):
        # Test calculating disk usage
        base_directory = os.path.join(self.test_dir, 'du_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')
        with open(os.path.join(base_directory, 'file2.txt'), 'w') as file2:
            file2.write('Content of file2')

        # Perform the du operation
        du_result = fs.du(base_directory, total=True, withdirs=True)

        # Check if the result contains the expected disk usage
        expected_du_result = os.path.getsize(os.path.join(base_directory, 'file1.txt')) + os.path.getsize(os.path.join(base_directory, 'file2.txt'))

        self.assertEqual(du_result, expected_du_result)

    def test_glob(self):
        # Test using glob to find files
        base_directory = os.path.join(self.test_dir, 'glob_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')
        with open(os.path.join(base_directory, 'file2.txt'), 'w') as file2:
            file2.write('Content of file2')

        # Perform the glob operation
        glob_result = fs.glob(os.path.join(base_directory, '*.txt'))

        # Check if the result contains the expected files
        expected_glob_result = [
            os.path.join(base_directory, 'file1.txt'),
            os.path.join(base_directory, 'file2.txt')
        ]

        self.assertEqual(sorted(glob_result), sorted(expected_glob_result))

    def test_exists(self):
        # Test checking if a file or directory exists
        base_directory = os.path.join(self.test_dir, 'exists_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Check if the files and directories exist
        self.assertTrue(fs.exists(base_directory))
        self.assertTrue(fs.exists(os.path.join(base_directory, 'dir1')))
        self.assertTrue(fs.exists(os.path.join(base_directory, 'file1.txt')))
        self.assertFalse(fs.exists(os.path.join(base_directory, 'nonexistent.txt')))

    def test_info(self):
        # Test getting information about a file or directory
        base_directory = os.path.join(self.test_dir, 'info_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Perform the info operation
        info_result = fs.info(base_directory, convert_date=True)

        # Check if the result contains the expected information
        self.assertTrue('created' in info_result)
        self.assertTrue('mtime' in info_result)
        self.assertTrue('type' in info_result)

    def test_checksum(self):
        # Test calculating the checksum of a file
        base_directory = os.path.join(self.test_dir, 'checksum_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Perform the checksum operation
        checksum_result = fs.checksum(os.path.join(base_directory, 'file1.txt'))

        # Check if the result contains the expected checksum
        expected_checksum_result = 'a174c891fc4ee62c6efa9b4eab5226c3'

        self.assertEqual(checksum_result, expected_checksum_result)

    def test_size(self):
        # Test getting the size of a file
        base_directory = os.path.join(self.test_dir, 'size_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Perform the size operation
        size_result = fs.size(os.path.join(base_directory, 'file1.txt'))

        # Check if the result contains the expected size
        expected_size_result = os.path.getsize(os.path.join(base_directory, 'file1.txt'))

        self.assertEqual(size_result, expected_size_result)

    def test_sizes(self):
        # Test getting the sizes of multiple files
        base_directory = os.path.join(self.test_dir, 'sizes_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')
        with open(os.path.join(base_directory, 'file2.txt'), 'w') as file2:
            file2.write('Content of file2')

        # Perform the sizes operation
        sizes_result = fs.sizes([os.path.join(base_directory, 'file1.txt'), os.path.join(base_directory, 'file2.txt')])

        # Check if the result contains the expected sizes
        expected_sizes_result = {
            os.path.join(base_directory, 'file1.txt'): os.path.getsize(os.path.join(base_directory, 'file1.txt')),
            os.path.join(base_directory, 'file2.txt'): os.path.getsize(os.path.join(base_directory, 'file2.txt'))
        }

        self.assertEqual(sizes_result, expected_sizes_result)

    def test_isdir(self):
        # Test checking if a path is a directory
        base_directory = os.path.join(self.test_dir, 'isdir_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Check if the paths are directories or not
        self.assertTrue(fs.isdir(base_directory))
        self.assertTrue(fs.isdir(os.path.join(base_directory, 'dir1')))
        self.assertFalse(fs.isdir(os.path.join(base_directory, 'file1.txt')))
        self.assertFalse(fs.isdir(os.path.join(base_directory, 'nonexistent')))

    def test_isfile(self):
        # Test checking if a path is a file
        base_directory = os.path.join(self.test_dir, 'isfile_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create some directories and files
        os.makedirs(os.path.join(base_directory, 'dir1', 'subdir'), exist_ok=True)
        with open(os.path.join(base_directory, 'file1.txt'), 'w') as file1:
            file1.write('Content of file1')

        # Check if the paths are files or not
        self.assertFalse(fs.isfile(base_directory))
        self.assertFalse(fs.isfile(os.path.join(base_directory, 'dir1')))
        self.assertTrue(fs.isfile(os.path.join(base_directory, 'file1.txt')))
        self.assertFalse(fs.isfile(os.path.join(base_directory, 'nonexistent.txt')))

    def test_read_text(self):
        # Test reading text from a file
        base_directory = os.path.join(self.test_dir, 'read_text_directory')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Create a file with content
        file_path = os.path.join(base_directory, 'file1.txt')
        with open(file_path, 'w') as file1:
            file1.write('Content of file1')

        # Perform the read_text operation
        read_text_result = fs.read_text(file_path)

        # Check if the result matches the expected content
        expected_read_text_result = 'Content of file1'

        self.assertEqual(read_text_result, expected_read_text_result)

    def test_write_text(self):
        # Test writing text to a file
        file_path = os.path.join(self.test_dir, 'path', 'to', 'test_file.txt')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs)

        # Perform the write_text operation
        fs.write_text(file_path, 'This is some text content.')

        # Check if the content is written successfully
        with self.local_fs.open(file_path, 'rt') as file:
            written_content = file.read()

        self.assertEqual('This is some text content.', written_content)

    def test_copy(self):
        # Test copying a file from source to destination
        source_path = os.path.join(self.test_dir, 'path', 'to', 'source.txt')
        destination_path = os.path.join(self.test_dir, 'path', 'to', 'destination.txt')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs, destination_fs=self.local_fs)

        # Perform the copy operation
        fs.copy(source_path, destination_path)

        # Check if the content is copied successfully
        with self.local_fs.open(destination_path, 'rb') as destination_file:
            copied_content = destination_file.read()

        self.assertEqual(b'', copied_content)

    def test_move(self):
        # Test moving a file from source to destination
        source_path = os.path.join(self.test_dir, 'path', 'to', 'source.txt')
        destination_path = os.path.join(self.test_dir, 'path', 'to', 'destination.txt')

        # Create the source file with some content
        with self.local_fs.open(source_path, 'wb') as source_file:
            source_file.write(b'This is the source file content.')

        # Create FileSystem instance with a real filesystem
        fs = FileSystem(source_fs=self.local_fs, destination_fs=self.local_fs)

        # Perform the move operation
        fs.move(source_path, destination_path)

        # Check if the content is moved successfully (source file should not exist)
        self.assertFalse(self.local_fs.exists(source_path))
        self.assertTrue(self.local_fs.exists(destination_path))

        # Check if the content is moved successfully
        with self.local_fs.open(destination_path, 'rb') as destination_file:
            moved_content = destination_file.read()

        self.assertEqual(b'This is the source file content.', moved_content)

if __name__ == '__main__':
    unittest.main()
