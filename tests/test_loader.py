import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from genai_inchoate_data.data_loader.loader import Loader

class TestLoader(unittest.TestCase):

    @patch("genai_inchoate_data.utilities.file_reader.FileReader")
    @patch("genai_inchoate_data.data_store.store.Store")
    @patch("genai_inchoate_data.utilities.file_reader.get_file_system")
    @patch("genai_inchoate_data.utilities.file_system.FileSystem")
    def test_init(self, mock_file_system, mock_get_file_system, mock_store, mock_file_reader):
        config_file = "test_config.json"
        loader = Loader(config_file)

        mock_file_reader.assert_called_once_with(config_file)
        mock_get_file_system.assert_not_called()
        mock_store.assert_called_once_with().get(loader.config_details.store)

    @patch("genai_inchoate_data.utilities.file_reader..get_file_system")
    @patch("genai_inchoate_data.utilities.file_system.FileSystem")
    def test_load(self, mock_file_system, mock_get_file_system):
        loader = Loader({"store": "mock_store", "source_file_system": "mock_source_fs", "target_file_system": "mock_target_fs",
                         "source_location": "mock_source_location", "target_location": "mock_target_location",
                         "write_metadata": True})

        mock_source_fs = MagicMock()
        mock_target_fs = MagicMock()
        mock_file_system.side_effect = [mock_source_fs, mock_target_fs]

        mock_fs = MagicMock()
        mock_file_system.return_value = mock_fs

        mock_metadata = {"mock_key": "mock_value"}
        mock_fs.info.return_value = mock_metadata

        mock_store = MagicMock()
        loader.store = mock_store

        loader.load()

        mock_get_file_system.assert_any_call("mock_source_fs")
        mock_get_file_system.assert_any_call("mock_target_fs")
        mock_file_system.assert_has_calls([mock.call("mock_source_fs"), mock.call("mock_target_fs")])

        mock_fs.copy.assert_called_once_with("mock_source_location", "mock_target_location")
        mock_fs.info.assert_called_once_with("mock_source_location")

        expected_data = {
            "_id": loader.load_details()["date"],  # Mocking uuid.uuid4() for simplicity
            "metadata": mock_metadata,
            "load_details": {"date": datetime.now().strftime("%Y-%m-%d"), "time": loader.load_details()["time"]}
        }
        mock_store.insert_document.assert_called_once_with("mock_store.collection_name", expected_data)

    def test_load_details(self):
        loader = Loader({"store": "mock_store"})
        details = loader.load_details()

        self.assertIn("date", details)
        self.assertIn("time", details)

if __name__ == '__main__':
    unittest.main()
