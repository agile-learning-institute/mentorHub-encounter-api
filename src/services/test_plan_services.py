import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime, timezone
from src.services.plan_services import PlanService


class TestPlanService(unittest.TestCase):

    @patch('src.utils.mongo_io.MongoIO.get_document')
    @patch('src.utils.mongo_io.MongoIO.create_document')
    def test_create_plan(self, mock_create_document, mock_get_document):
        mock_create_document.return_value = "mock_plan_id"
        mock_get_document.return_value = {"id": ObjectId("000000000000000000000001"), "status": "Active"}

        data = {"name": "Foo"}
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        breadcrumb = {"atTime": datetime.now(timezone.utc),"byUser": ObjectId(),"fromIp": "127.0.0.1","correlationId": "test-correlation-id"}

        result = PlanService.create_plan(data, token, breadcrumb)
        self.assertEqual(result, {"id": ObjectId("000000000000000000000001"), "status": "Active"})

        # Assertions for MongoIO interactions
        mock_create_document.assert_called_once_with(
            "plans",
            {
                "name": "Foo",
                "lastSaved": breadcrumb,
                "status": "Active"
            }
        )
        mock_get_document.assert_called_once_with("plans", "mock_plan_id")

    @patch('src.utils.mongo_io.MongoIO.get_document')
    def test_get_plan(self, mock_get_document):
        mock_get_document.side_effect = [{"name": "foo"}]

        plan_id = "mock_plan_id"
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}

        result = PlanService.get_plan(plan_id, token)
        self.assertEqual(result, {"name": "foo"})

        # Assertions for MongoIO interactions
        mock_get_document.assert_called_with("plans", plan_id)

    @patch('src.utils.mongo_io.MongoIO.update_document')
    def test_update_plan(self, mock_update_document):
        test_document = {"name":"foo"}
        mock_update_document.side_effect = [test_document]

        plan_id = "mock_plan_id"
        patch_data = {"status": "Updated"}
        token = {"user_id": str(ObjectId()), "roles": ["Staff"]}
        breadcrumb = {"atTime": datetime.now(timezone.utc),"byUser": ObjectId(),"fromIp": "127.0.0.1","correlationId": "test-correlation-id"}

        result = PlanService.update_plan(plan_id, patch_data, token, breadcrumb)
        self.assertEqual(result, test_document)

        # Assertions for MongoIO interactions
        mock_update_document.assert_called_once_with(
            "plans",
            "mock_plan_id",
            {"status": "Updated", "lastSaved": breadcrumb}
        )

    def test_check_user_access_staff(self):
        token = {"roles": ["Staff"]}
        try:
            PlanService._check_user_access(token)
        except Exception:
            self.fail("_check_user_access raised Exception unexpectedly!")

    def test_check_user_access_mentor(self):
        token = {"roles": ["Mentor"]}
        try:
            PlanService._check_user_access(token)
        except Exception:
            self.fail("_check_user_access raised Exception unexpectedly!")

    def test_check_user_access_access_denied(self):
        token = {"roles": ["Member"]}
        with self.assertRaises(Exception) as context:
            PlanService._check_user_access(token)
        self.assertEqual(str(context.exception), "Access Denied")


if __name__ == '__main__':
    unittest.main()