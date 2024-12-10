import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from datetime import datetime, timezone
from src.services.plan_services import planService


class TestPersonService(unittest.TestCase):

    @patch('src.utils.mongo_io.MongoIO.get_documents')
    def test_get_people(self, mock_get_documents):
        self.assertEqual(False, True)

    @patch('src.utils.mongo_io.MongoIO.get_documents')
    def test_get_mentors(self, mock_get_documents):
        self.assertEqual(False, True)

if __name__ == '__main__':
    unittest.main()