import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.routes.encounter_routes import create_encounter_routes
from src.utils.ejson_encoder import MongoJSONEncoder

class TestencounterRoutes(unittest.TestCase):

    def setUp(self):
        # Test Data
        self.sample_encounter = {"TODO - Define Sample Data"}
        
        # Set up the Flask test app and register the blueprint
        self.app = Flask(__name__)
        self.app.json = MongoJSONEncoder(self.app)        
        encounter_routes = create_encounter_routes()
        self.app.register_blueprint(encounter_routes, url_prefix='/api/encounter')
        self.client = self.app.test_client()

    @patch('src.routes.encounter_routes.encounterService.create_encounter')
    def test_create_encounter_success(self, mock_create):
        # Mock the encounterService's get_or_create_encounter method
        mock_create.return_value = self.sample_encounter

        response = self.client.post('/api/encounter/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

        data = response.get_json()
        self.assertEqual(data, self.sample_encounter)

    # TODO: Write more tests

if __name__ == '__main__':
    unittest.main()