import copy
from datetime import datetime, timezone
import unittest
from unittest.mock import patch

from bson import ObjectId
from src.services.encounter_services import encounterService
from src.utils.mongo_io import MongoIO

class TestencounterService(unittest.TestCase):
    
    def setUp(self):    
        self.maxDiff = None

        # Setup Test Data
        token = {}
        # TODO token for RBAC testing
        # TODO Additional test data as needed
        
    @patch('src.services.encounter_services.MongoIO')
    def test_create_encounter_success(self, mock_mongo_io):
        # Mock the MongoIO methods
        mock_instance = mock_mongo_io.return_value
        mock_instance.get_encounter.return_value = self.test_encounter_one
        mock_instance.get_mentor.return_value = "eeee00000000000000000001"

        encounter = encounterService.get_or_create_encounter("eeee00000000000000000001", self.token, self.breadcrumb)
        mock_instance.get_encounter.assert_called_once_with("eeee00000000000000000001")
        self.assertEqual(encounter, self.test_encounter_one)
        mock_instance.reset_mock()

    # TODO Write more tests

if __name__ == '__main__':
    unittest.main()