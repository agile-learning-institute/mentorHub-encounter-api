import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime, timezone

from mentorhub_utils import MentorHub_Config
from src.services.encounter_services import EncounterService


class TestEncounterService(unittest.TestCase):

    def setUp(self):    
        # Setup Test Data
        self.token = {"user_id":"ObjectID", "roles":["Staff"]}
        self.breadcrumb = {"atTime":datetime.fromisoformat("2024-08-01T12:00:00"),"byUser":ObjectId("aaaa00000000000000000001"),"fromIp":"127.0.0.1","correlationId":"aaaa-aaaa-aaaa-aaaa"}

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_token_staff(self, mock_get_instance):
        config = MentorHub_Config.get_instance()
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"foo": "bar"}
        
        curriculum = EncounterService.get_encounter("encounter_id", self.token)
        mock_mongo_io.get_document.assert_called_once_with(config.ENCOUNTERS_COLLECTION_NAME, "encounter_id")
        self.assertEqual(curriculum, {"foo": "bar"})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_token_member_pass(self, mock_get_instance):
        config = MentorHub_Config.get_instance()
        token = {"user_id":"000000000000000000000000", "roles":["Member"]}
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"foo": "bar"}

        curriculum = EncounterService.get_encounter("000000000000000000000000", token)
        mock_mongo_io.get_document.assert_called_once_with(config.ENCOUNTERS_COLLECTION_NAME, "000000000000000000000000")
        self.assertEqual(curriculum, {"foo": "bar"})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_token_member_fail(self, mock_get_instance):
        token = {"user_id":"000000000000000000000001", "roles":["Member"]}
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"foo": "bar"}

        with self.assertRaises(Exception) as context:
            EncounterService.get_encounter("", {}, {})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_token_mentor_pass(self, mock_get_instance):
        config = MentorHub_Config.get_instance()
        token = {"user_id":"000000000000000000000012", "roles":["Mentor"]}
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.side_effect = [
            {"mentorId": "000000000000000000000012"},
            {"foo": "bar"}
        ]

        curriculum = EncounterService.get_encounter("000000000000000000000000", token)
        mock_mongo_io.get_document.assert_has_calls([
            unittest.mock.call(config.PEOPLE_COLLECTION_NAME, "000000000000000000000000"),
            unittest.mock.call(config.ENCOUNTERS_COLLECTION_NAME, "000000000000000000000000")
        ])
        self.assertEqual(curriculum, {"foo": "bar"})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_token_mentor_fail(self, mock_get_instance):
        token = {"user_id":"000000000000000000000012", "roles":["Mentor"]}
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"mentorId": "000000000000000000001234"}

        with self.assertRaises(Exception) as context:
            EncounterService.get_encounter("", {}, {})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_create_encounter(self, mock_get_instance):
        config = MentorHub_Config.getInstance()
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = {"foo":"bar"}
        mock_mongo_io.create_document.return_value = "mock_encounter_id"

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

        result = EncounterService.create_encounter(data, token, breadcrumb)
        self.assertEqual(result, {"foo":"bar"})
        
        # Assertions for MongoIO interactions
        mock_mongo_io.create_document.assert_called_once_with(
            config.ENCOUNTERS_COLLECTION_NAME,
            {
                "personId": ObjectId(data["personId"]),
                "mentorId": ObjectId(data["mentorId"]),
                "planId": ObjectId(data["planId"]),
                "status": "Active",
                "lastSaved": breadcrumb
            }
        )
        mock_mongo_io.get_document.assert_called_once_with(
            config.ENCOUNTERS_COLLECTION_NAME, "mock_encounter_id")

    @patch('mentorhub_utils.MentorHubMongoIO.get_document')
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

        result = EncounterService.get_encounter(encounter_id, token)
        self.assertEqual(result, test_document)

        # Assertions for MongoIO interactions
        mock_get_document.assert_called_with("encounters", encounter_id)

    @patch('mentorhub_utils.MentorHubMongoIO.get_document')
    @patch('mentorhub_utils.MentorHubMongoIO.update_document')
    def test_update_encounter(self, mock_update_document, mock_get_document):
        test_document = {"personId": ObjectId(), "mentorId": ObjectId(), "plan_id": ObjectId()}
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

        result = EncounterService.update_encounter(encounter_id, patch_data, token, breadcrumb)
        self.assertEqual(result, test_document)

        # Assertions for MongoIO interactions
        mock_get_document.assert_called_with("encounters", encounter_id)
        mock_update_document.assert_called_once_with(
            "encounters",
            encounter_id,
            {"status": "Updated", "lastSaved": breadcrumb}
        )

    def test_check_user_access_staff(self):
        data = {"personId": str(ObjectId()), "mentor_id": str(ObjectId())}
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        try:
            EncounterService._check_user_access(data, token)
        except Exception:
            self.fail("_check_user_access raised Exception unexpectedly!")

    def test_check_user_access_access_denied(self):
        data = {"personId": str(ObjectId()), "mentor_id": str(ObjectId())}
        token = {"user_id": str(ObjectId()), "roles": ["Member"]}
        with self.assertRaises(Exception) as context:
            EncounterService._check_user_access(data, token)
        self.assertEqual(str(context.exception), "Access Denied")


if __name__ == '__main__':
    unittest.main()