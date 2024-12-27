import unittest
from unittest.mock import patch
from flask import Flask
from src.routes.people_routes import create_people_routes
from mentorhub_utils import MongoJSONEncoder

class TestPeopleRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)

        people_routes = create_people_routes()
        self.app.register_blueprint(people_routes, url_prefix='/api/people')
        self.client = self.app.test_client()

    @patch('src.services.person_services.PersonService.get_people')
    def test_get_people_success(self, mock_get_people):
        mock_get_people.return_value = {"foo": "bar"}

        response = self.client.get('/api/people/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, {"foo": "bar"})
        
    @patch('src.services.person_services.PersonService.get_people')
    def test_get_people_error(self, mock_get_people):
        mock_get_people.side_effect = Exception('Test error')
        response = self.client.get('/api/people/', json={'foo': 'bar'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()