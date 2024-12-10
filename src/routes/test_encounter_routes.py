import unittest
from unittest.mock import patch
from flask import Flask
from src.routes.encounter_routes import create_encounter_routes
from bson import ObjectId

class TestEncounterRoutes(unittest.TestCase):

    def setUp(self):
        # Set up Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(create_encounter_routes(), url_prefix='/api/encounter')
        self.client = self.app.test_client()

    @patch('src.services.encounter_services.encounterService.create_encounter')
    def test_create_encounter(self, mock_create_encounter):
        # Mock the response from encounterService.create_encounter
        mock_create_encounter.return_value = {'id': 'mock_id', 'status': 'created'}

        request_data = {'name': 'Test Encounter'}
        response = self.client.post('/api/encounter/', json=request_data)

        # Assertions for response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 'mock_id', 'status': 'created'})

    @patch('src.services.encounter_services.encounterService.create_encounter')
    def test_breadcrumb_with_create_encounter(self, mock_create_encounter):
        # Mock the response from encounterService.create_encounter
        mock_create_encounter.return_value = {'id': 'mock_id', 'status': 'created'}

        # Send POST request with headers for breadcrumb
        headers = {
            'X-User-Id': str(ObjectId()),  # Mock a valid user ID
            'X-Correlation-Id': 'test-correlation-id'
        }
        request_data = {'name': 'Test Encounter'}
        response = self.client.post('/api/encounter/', json=request_data, headers=headers)

        # Verify that the correct breadcrumb is passed
        actual_breadcrumb = mock_create_encounter.call_args[0][2]
        expected_breadcrumb = {
            'byUser': ObjectId(headers['X-User-Id']),
            'correlationId': 'test-correlation-id'
        }
        self.assertEqual(actual_breadcrumb['byUser'], expected_breadcrumb['byUser'])
        self.assertEqual(actual_breadcrumb['correlationId'], expected_breadcrumb['correlationId'])

    @patch('src.services.encounter_services.encounterService.create_encounter')
    def test_token_with_create_encounter(self, mock_create_encounter):
        # Mock the response from encounterService.create_encounter
        mock_create_encounter.return_value = {'id': 'mock_id', 'status': 'created'}

        # Send POST request with headers for breadcrumb
        headers = {
            'X-User-Id': str(ObjectId()),  # Mock a valid user ID
            'X-Correlation-Id': 'test-correlation-id'
        }
        request_data = {'name': 'Test Encounter'}
        response = self.client.post('/api/encounter/', json=request_data, headers=headers)

        # Verify the token passed
        expected_token = {
            "user_id": "aaaa00000000000000000001",
            "roles": ["Staff"]
        }
        self.assertEqual(mock_create_encounter.call_args[0][1], expected_token)

    @patch('src.services.encounter_services.encounterService.create_encounter', side_effect=Exception('Test error'))
    def test_create_encounter_error(self, mock_create_encounter):
        response = self.client.post('/api/encounter/', json={'name': 'Test Encounter'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.services.encounter_services.encounterService.get_encounter')
    def test_get_encounter(self, mock_get_encounter):
        # Mock the response from encounterService.get_encounter
        mock_get_encounter.return_value = {'id': 'mock_id', 'name': 'Test Encounter'}

        response = self.client.get('/api/encounter/mock_id')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 'mock_id', 'name': 'Test Encounter'})


    @patch('src.services.encounter_services.encounterService.get_encounter', side_effect=Exception('Test error'))
    def test_get_encounter_error(self, mock_get_encounter):
        response = self.client.get('/api/encounter/mock_id')

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.services.encounter_services.encounterService.update_encounter')
    def test_update_encounter(self, mock_update_encounter):
        # Mock the response from encounterService.update_encounter
        mock_update_encounter.return_value = {'id': 'mock_id', 'status': 'updated'}

        request_data = {'status': 'updated'}
        response = self.client.patch('/api/encounter/mock_id', json=request_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 'mock_id', 'status': 'updated'})

    @patch('src.services.encounter_services.encounterService.update_encounter', side_effect=Exception('Test error'))
    def test_update_encounter_error(self, mock_update_encounter):
        request_data = {'status': 'updated'}
        response = self.client.patch('/api/encounter/mock_id', json=request_data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})


if __name__ == '__main__':
    unittest.main()