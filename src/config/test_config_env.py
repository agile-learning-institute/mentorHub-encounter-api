import unittest
import os
from src.config.Config import config

class TestConfigEnvironment(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Class-level setup: Initialize configuration items"""
        cls.public_config_items = [
            "BUILT_AT", "CONFIG_FOLDER", "PORT", "DB_NAME",
            "VERSION_COLLECTION_NAME", "ENUMERATORS_COLLECTION_NAME", 
            "ENCOUNTERS_COLLECTION_NAME", "PLANS_COLLECTION_NAME" 
        ]
        
        cls.secret_config_items = [
            "CONNECTION_STRING"
        ]
        
    def setUp(self):
        """Re-initialize the config for each test."""
        # Set all environment variables to "ENV_VALUE"
        for var in self.public_config_items + self.secret_config_items:
            os.environ[var] = "9999"

        # Initialize the Config object
        config.initialize()
        
        # Reset environment variables 
        for var in self.public_config_items + self.secret_config_items:
            if os.environ[var]:
                del os.environ[var]

    def test_environment_properties_in_getters(self):
        self.assertEqual(config.get_config_folder(), "9999")
        self.assertEqual(config.get_port(), 9999)
        self.assertEqual(config.get_version_collection_name(), "9999")
        self.assertEqual(config.get_enumerators_collection_name(), "9999")
        self.assertEqual(config.get_encounters_collection_name(), "9999")
        self.assertEqual(config.get_plans_collection_name(), "9999")
        self.assertEqual(config.get_connection_string(), "9999")
        self.assertEqual(config.get_db_name(), "9999")

    def test_environment_public_config_items(self):
        for item in self.public_config_items:
            self._test_config_environment_value(item, "9999")

    def test_environment_secret_config_items(self):
        for item in self.secret_config_items:
            self._test_config_environment_value(item, "secret")

    def _test_config_environment_value(self, config_name, config_value):
        """Helper function to check environment values."""
        items = config.config_items
        item = next((i for i in items if i['name'] == config_name), None)
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], config_name)
        self.assertEqual(item['from'], "environment")
        self.assertEqual(item['value'], config_value)

if __name__ == '__main__':
    unittest.main()