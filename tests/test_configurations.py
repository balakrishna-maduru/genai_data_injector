import unittest
from genai_inchoate_data.utilities.configurations import Configurations

class TestConfigurations(unittest.TestCase):
    def setUp(self):
        # Test data
        self.config_data = {
            "name": "John",
            "age": 25,
            "address": {
                "city": "New York",
                "zip": "10001"
            }
        }

        # Create a Configurations instance for testing
        self.config_obj = Configurations(self.config_data)

    def test_get_top_level_property(self):
        self.assertEqual(self.config_obj.name, "John")
        self.assertEqual(self.config_obj.age, 25)

    def test_get_nested_property(self):
        self.assertEqual(self.config_obj.address.city, "New York")
        self.assertEqual(self.config_obj.address.zip, "10001")

    def test_set_top_level_property(self):
        with self.assertRaises(ValueError) as context:
            self.config_obj.name = "Alice"

        # Optional: Check the error message if needed
        error_message = str(context.exception)
        self.assertIn("The value for the nested key 'name' must be an instance of Configurations or None", error_message)


    def test_set_nested_property(self):
        nested_config = Configurations({"city": "San Francisco", "zip": "94105"})
        self.config_obj.address = nested_config
        self.assertEqual(self.config_obj.address.city, "San Francisco")
        self.assertEqual(self.config_obj.address.zip, "94105")

        # Setting the nested property to None should also work
        self.config_obj.address = None
        self.assertIsNone(self.config_obj.address)

    def test_set_nested_property_with_correct_type(self):
        nested_config = Configurations({"city": "Los Angeles", "zip": "90001"})
        self.config_obj.address = nested_config
        self.assertEqual(self.config_obj.address.city, "Los Angeles")
        self.assertEqual(self.config_obj.address.zip, "90001")

    def test_access_nonexistent_property(self):
        with self.assertRaises(AttributeError):
            print(self.config_obj.nonexistent_property)

    def test_access_nonexistent_nested_property(self):
        with self.assertRaises(AttributeError):
            print(self.config_obj.address.nonexistent_property)

    def test_set_nonexistent_nested_property(self):
        with self.assertRaises(AttributeError):
            self.config_obj.nonexistent_property.nonexistent_nested_property = "New Value"

if __name__ == '__main__':
    unittest.main()
