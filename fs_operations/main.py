# main.py
from extension_mapper import ExtensionMapper
from folder import Folder
from file_system import FileSystem

# Example usage
if __name__ == "__main__":

    root_folder = Folder()

    # Add files to the root folder dynamically
    root_folder.add_file('/Users/balakrishnamaduru/Documents/git/file_reader/tests/resources/sample.txt')

    # Read files and print results
    root_folder.read()

    # Print the results
    for file_name, content in root_folder.results.items():
        print(f"{file_name}:\n{content}")
