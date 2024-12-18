import unittest
from unittest.mock import patch
from flask import Flask
from src.routes.mentor_routes import create_mentor_routes
from src.routes.ejson_encoder import MongoJSONEncoder

class TestMentorRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)

        mentor_routes = create_mentor_routes()
        self.app.register_blueprint(mentor_routes, url_prefix='/api/mentors')
        self.client = self.app.test_client()

    @patch('src.services.person_services.PersonService.get_mentors')
    def test_get_mentor_success(self, mock_get_mentors):
        mock_get_mentors.return_value = {"foo": "bar"}

        response = self.client.get('/api/mentors/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, {"foo": "bar"})
        
    @patch('src.services.person_services.PersonService.get_mentors')
    def test_get_mentor_error(self, mock_get_mentors):
        mock_get_mentors.side_effect = Exception('Test error')
        response = self.client.get('/api/mentors/', json={'foo': 'bar'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()