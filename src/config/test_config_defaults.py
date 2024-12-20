import unittest
from src.config.config import config

class TestConfigDefaults(unittest.TestCase):

    def setUp(self):
        """Re-initialize the config for each test."""
        config.initialize()

    def test_default_properties_in_getters(self):
        self.assertEqual(config.api_version, "1.0.LOCAL")
        self.assertEqual(config.CONFIG_FOLDER, "/opt/mentorhub-encounter-api")
        self.assertEqual(config.PORT, 8088)
        self.assertEqual(config.VERSION_COLLECTION_NAME, "msmCurrentVersions")
        self.assertEqual(config.ENUMERATORS_COLLECTION_NAME, "enumerators")
        self.assertEqual(config.ENCOUNTERS_COLLECTION_NAME, "encounters")
        self.assertEqual(config.PLANS_COLLECTION_NAME, "plans")
        self.assertEqual(config.PEOPLE_COLLECTION_NAME, "people")
        self.assertEqual(config.CONNECTION_STRING, "mongodb://mongodb:27017/?replicaSet=rs0")
        self.assertEqual(config.DB_NAME, "mentorHub")
        
    def test_to_dict(self):
        """Test the to_dict method of the Config class."""
        expected_dict = {
            "api_version": "1.0.LOCAL",
            "versions": [],
            "enumerators": {},
        }

        # Config Items are tested elsewhere
        result_dict = config.to_dict()
        result_dict.pop("config_items", None)
        self.assertEqual(result_dict, expected_dict)
        
    def test_default_config_items(self):
        self._test_config_default_value("BUILT_AT", "LOCAL")
        self._test_config_default_value("CONFIG_FOLDER", "/opt/mentorhub-encounter-api")
        self._test_config_default_value("PORT", "8088")
        self._test_config_default_value("VERSION_COLLECTION_NAME", "msmCurrentVersions")
        self._test_config_default_value("ENUMERATORS_COLLECTION_NAME", "enumerators")
        self._test_config_default_value("ENCOUNTERS_COLLECTION_NAME", "encounters")
        self._test_config_default_value("PLANS_COLLECTION_NAME", "plans")
        self._test_config_default_value("PEOPLE_COLLECTION_NAME", "people")
        self._test_config_default_value("CONNECTION_STRING", "secret")
        self._test_config_default_value("DB_NAME", "mentorHub")

    def _test_config_default_value(self, config_name, expected_value):
        """Helper function to check default values."""
        items = config.config_items
        item = next((i for i in items if i['name'] == config_name), None)
        self.assertIsNotNone(item)
        self.assertEqual(item['name'], config_name)
        self.assertEqual(item['from'], "default")
        self.assertEqual(item['value'], expected_value)

if __name__ == '__main__':
    unittest.main()