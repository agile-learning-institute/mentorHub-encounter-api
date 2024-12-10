import unittest
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

    # @patch('src.utils.mongoIO.get_documents', side_effect={"foo":"bar"})
    def test_get_mentor_success(self):
        # Simulate a GET request to the /api/mentors endpoint
        response = self.client.get('/api/mentors/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertIsInstance(data, dict)
        # TODO: Match get_documents side effect. 

    # @patch('src.utils.mongoIO.get_documents', side_effect=Exception('Test error'))
    def test_get_mentor_error(self, mock_create_encounter):
        response = self.client.post('/api/mentors/', json={'foo': 'bar'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

if __name__ == '__main__':
    unittest.main()