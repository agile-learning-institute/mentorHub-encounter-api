import unittest
from unittest.mock import patch, MagicMock
from src.services.person_services import PersonService

class TestPersonService(unittest.TestCase):

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_people_staff_access(self, mock_get_instance):
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_document.return_value = [{"_id": "123", "firstName": "John", "lastName": "Doe"}]

        token = {"roles": ["Staff"], "userId": "staff1"}
        result = PersonService.get_people(token)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["firstName"], "John")
        mock_mongo_io.get_document.assert_called_once_with("people", {}, {"firstName": 1, "lastName": 1, "_id": 1})

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_people_mentor_access(self, mock_get_instance):
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_documents.return_value = [{"_id": "123", "firstName": "John", "lastName": "Doe"}]

        token = {"roles": ["Mentor"], "userId": "mentor1"}
        result = PersonService.get_people(token)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["firstName"], "John")
        mock_mongo_io.get_documents.assert_called_once_with("people", {"mentorId": "mentor1"}, {"firstName": 1, "lastName": 1, "_id": 1})

    def test_get_people_access_denied(self):
        token = {"roles": ["Student"], "userId": "student1"}
        
        with self.assertRaises(PermissionError) as cm:
            PersonService.get_people(token)
        
        self.assertEqual(str(cm.exception), "Access Denied!")

    @patch('mentorhub_utils.MentorHubMongoIO.get_instance')
    def test_get_mentors(self, mock_get_instance):
        mock_mongo_io = MagicMock()
        mock_get_instance.return_value = mock_mongo_io
        mock_mongo_io.get_documents.return_value = [{"_id": "123", "firstName": "Jane", "lastName": "Smith"}]

        token = {"roles": ["Staff"], "userId": "staff1"}
        result = PersonService.get_mentors(token)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["firstName"], "Jane")
        mock_mongo_io.get_documents.assert_called_once_with("people", {"roles": {"$in": ["mentor"]}}, {"firstName": 1, "lastName": 1, "_id": 1})

if __name__ == '__main__':
    unittest.main()