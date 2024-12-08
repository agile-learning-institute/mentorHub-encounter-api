import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime, timezone
from src.services.encounter_services import encounterService


class TestEncounterService(unittest.TestCase):

    @patch('src.utils.mongo_io.MongoIO.get_document')
    @patch('src.utils.mongo_io.MongoIO.create_document')
    def test_create_encounter(self, mock_create_document, mock_get_document):
        mock_create_document.return_value = "mock_encounter_id"
        mock_get_document.return_value = {"id": "mock_encounter_id", "status": "Active"}

        data = {
            "personId": str(ObjectId()),
            "mentorId": str(ObjectId()), 
            "planId": str(ObjectId())
        }
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        breadcrumb = {
            "atTime": datetime.now(timezone.utc),
            "byUser": ObjectId(),
            "fromIp": "127.0.0.1",
            "correlationId": "test-correlation-id"
        }

        result = encounterService.create_encounter(data, token, breadcrumb)

        # Assertions for MongoIO interactions
        mock_create_document.assert_called_once_with(
            "encounters",
            {
                "personId": ObjectId(data["personId"]),
                "mentorId": ObjectId(data["mentorId"]),
                "planId": ObjectId(data["planId"]),
                "status": "Active",
                "lastSaved": breadcrumb
            }
        )
        mock_get_document.assert_called_once_with("mock_encounter_id")
        self.assertEqual(result, {"id": "mock_encounter_id", "status": "Active"})

    @patch('src.utils.mongo_io.MongoIO.get_document')
    def test_get_encounter(self, mock_get_document):
        test_document = {"personId": str(ObjectId()), "mentorId": str(ObjectId()), "planId": str(ObjectId())}
        mock_get_document.side_effect = [test_document]

        encounter_id = "mock_encounter_id"
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        breadcrumb = {
            "atTime": datetime.now(timezone.utc),
            "byUser": ObjectId(),
            "fromIp": "127.0.0.1",
            "correlationId": "test-correlation-id"
        }

        result = encounterService.get_encounter(encounter_id, token)

        # Assertions for MongoIO interactions
        mock_get_document.assert_called_with("encounters", encounter_id)
        self.assertEqual(result, test_document)

    @patch('src.utils.mongo_io.MongoIO.get_document')
    @patch('src.utils.mongo_io.MongoIO.update_document')
    def test_update_encounter(self, mock_update_document, mock_get_document):
        test_document = {"personId": str(ObjectId()), "mentorId": str(ObjectId()), "plan_id": str(ObjectId())}
        mock_get_document.side_effect = [test_document]
        mock_update_document.side_effect = [test_document]

        encounter_id = "mock_encounter_id"
        patch_data = {"status": "Updated"}
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        breadcrumb = {
            "atTime": datetime.now(timezone.utc),
            "byUser": ObjectId(),
            "fromIp": "127.0.0.1",
            "correlationId": "test-correlation-id"
        }

        result = encounterService.update_encounter(encounter_id, patch_data, token, breadcrumb)

        # Assertions for MongoIO interactions
        mock_update_document.assert_called_once_with(
            "encounters",
            encounter_id,
            {"status": "Updated", "lastSaved": breadcrumb}
        )
        mock_get_document.assert_any_call(encounter_id)
        self.assertEqual(result, test_document)

    def test_check_user_access_staff(self):
        data = {"personId": str(ObjectId()), "mentor_id": str(ObjectId())}
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        try:
            encounterService._check_user_access(data, token)
        except Exception:
            self.fail("_check_user_access raised Exception unexpectedly!")

    def test_check_user_access_access_denied(self):
        data = {"personId": str(ObjectId()), "mentor_id": str(ObjectId())}
        token = {"user_id": str(ObjectId()), "roles": ["Member"]}
        with self.assertRaises(Exception) as context:
            encounterService._check_user_access(data, token)
        self.assertEqual(str(context.exception), "Access Denied")


if __name__ == '__main__':
    unittest.main()