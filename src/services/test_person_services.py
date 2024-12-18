import unittest
from unittest.mock import patch
from src.services.person_services import PersonService
from src.utils.mongo_io import mongoIO

class TestPersonService(unittest.TestCase):

    @patch('src.utils.mongo_io.mongoIO.get_documents')
    def test_get_people_staff_access(self, mock_get_documents):
        mock_get_documents.return_value = [{"_id": "123", "firstName": "John", "lastName": "Doe"}]

        token = {"roles": ["Staff"], "userId": "staff1"}
        result = PersonService.get_people(token)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["firstName"], "John")
        mock_get_documents.assert_called_once_with("people", {}, {"firstName": 1, "lastName": 1, "_id": 1})

    @patch('src.utils.mongo_io.mongoIO.get_documents')
    def test_get_people_mentor_access(self, mock_get_documents):
        mock_get_documents.return_value = [{"_id": "123", "firstName": "John", "lastName": "Doe"}]

        token = {"roles": ["Mentor"], "userId": "mentor1"}
        result = PersonService.get_people(token)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["firstName"], "John")
        mock_get_documents.assert_called_once_with("people", {"mentorId": "mentor1"}, {"firstName": 1, "lastName": 1, "_id": 1})

    def test_get_people_access_denied(self):
        token = {"roles": ["Student"], "userId": "student1"}
        
        with self.assertRaises(PermissionError) as cm:
            PersonService.get_people(token)
        
        self.assertEqual(str(cm.exception), "Access Denied!")

    @patch('src.utils.mongo_io.mongoIO.get_documents')
    def test_get_mentors(self, mock_get_documents):
        mock_get_documents.return_value = [{"_id": "123", "firstName": "Jane", "lastName": "Smith"}]

        token = {"roles": ["Staff"], "userId": "staff1"}
        result = PersonService.get_mentors(token)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["firstName"], "Jane")
        mock_get_documents.assert_called_once_with("people", {"roles": {"$in": ["mentor"]}}, {"firstName": 1, "lastName": 1, "_id": 1})

if __name__ == '__main__':
    unittest.main()