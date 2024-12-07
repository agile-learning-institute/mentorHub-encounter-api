import unittest
import os
from src.config.config import config

class TestConfigFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class-level setup: Initialize configuration items"""
        cls.public_config_items = [
            "PORT", "DB_NAME",
            "VERSION_COLLECTION_NAME", "ENUMERATORS_COLLECTION_NAME", 
            "ENCOUNTERS_COLLECTION_NAME", "PLANS_COLLECTION_NAME" 
        ]
        
        cls.secret_config_items = [
            "CONNECTION_STRING"
        ]
        
    def setUp(self):
        """Re-initialize the config for each test."""
        # Set Config Folder location and Initialize Config
        os.environ["CONFIG_FOLDER"] = "./test/resources/configTest"
        config.initialize()
        del os.environ["CONFIG_FOLDER"]

    def test_file_properties_in_getters(self):
        self.assertEqual(config.get_port(), 123456)
        self.assertEqual(config.get_version_collection_name(), "123456")
        self.assertEqual(config.get_enumerators_collection_name(), "123456")
        self.assertEqual(config.get_encounters_collection_name(), "123456")
        self.assertEqual(config.get_plans_collection_name(), "123456")
        self.assertEqual(config.get_connection_string(), "123456")
        self.assertEqual(config.get_db_name(), "123456")

    def test_public_file_config_items(self):
        for item in self.public_config_items:
            self._test_config_file_value(item, "123456")
        
    def test_private_file_config_items(self):
        for item in self.secret_config_items:
            self._test_config_file_value(item, "secret")

    def _test_config_file_value(self, config_name, config_value):
        """Helper function to check file values."""
        items = config.config_items
        item = next((i for i in items if i['name'] == config_name), None)
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], config_name)
        self.assertEqual(item['from'], "file")
        self.assertEqual(item['value'], config_value)

if __name__ == '__main__':
    unittest.main()