import unittest
from unittest.mock import patch
from flask import Flask
from src.routes.plan_routes import create_plan_routes
from bson import ObjectId

class TestEncounterRoutes(unittest.TestCase):

    def setUp(self):
        # Set up Flask app for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(create_plan_routes(), url_prefix='/api/plan')
        self.client = self.app.test_client()

    @patch('src.services.plan_services.PlanService.create_plan')
    def test_create_plan(self, mock_create_plan):
        # Mock the response from planService.create_plan
        mock_create_plan.return_value = {'id': 'mock_id', 'status': 'created'}

        request_data = {'name': 'Test Encounter'}
        response = self.client.post('/api/plan/', json=request_data)

        # Assertions for response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 'mock_id', 'status': 'created'})

    @patch('src.services.plan_services.PlanService.create_plan')
    def test_breadcrumb_with_create_plan(self, mock_create_plan):
        # Mock the response from planService.create_plan
        mock_create_plan.return_value = {'id': 'mock_id', 'status': 'created'}

        # Send POST request with headers for breadcrumb
        headers = {
            'X-User-Id': str(ObjectId()),  # Mock a valid user ID
            'X-Correlation-Id': 'test-correlation-id'
        }
        request_data = {'name': 'Test Encounter'}
        response = self.client.post('/api/plan/', json=request_data, headers=headers)

        # Verify that the correct breadcrumb is passed
        actual_breadcrumb = mock_create_plan.call_args[0][2]
        expected_breadcrumb = {
            'byUser': ObjectId(headers['X-User-Id']),
            'correlationId': 'test-correlation-id'
        }
        self.assertEqual(actual_breadcrumb['byUser'], expected_breadcrumb['byUser'])
        self.assertEqual(actual_breadcrumb['correlationId'], expected_breadcrumb['correlationId'])

    @patch('src.services.plan_services.planService.create_plan')
    def test_token_with_create_plan(self, mock_create_plan):
        # Mock the response from planService.create_plan
        mock_create_plan.return_value = {'id': 'mock_id', 'status': 'created'}

        # Send POST request with headers for breadcrumb
        headers = {
            'X-User-Id': str(ObjectId()),  # Mock a valid user ID
            'X-Correlation-Id': 'test-correlation-id'
        }
        request_data = {'name': 'Test Encounter'}
        response = self.client.post('/api/plan/', json=request_data, headers=headers)

        # Verify the token passed
        expected_token = {
            "user_id": "aaaa00000000000000000001",
            "roles": ["Staff"]
        }
        self.assertEqual(mock_create_plan.call_args[0][1], expected_token)

    @patch('src.services.plan_services.planService.create_plan', side_effect=Exception('Test error'))
    def test_create_plan_error(self, mock_create_plan):
        response = self.client.post('/api/plan/', json={'name': 'Test Encounter'})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.services.plan_services.planService.get_plan')
    def test_get_plan(self, mock_get_plan):
        # Mock the response from planService.get_plan
        mock_get_plan.return_value = {'id': 'mock_id', 'name': 'Test Encounter'}

        response = self.client.get('/api/plan/mock_id')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 'mock_id', 'name': 'Test Encounter'})


    @patch('src.services.plan_services.planService.get_plan', side_effect=Exception('Test error'))
    def test_get_plan_error(self, mock_get_plan):
        response = self.client.get('/api/plan/mock_id')

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})

    @patch('src.services.plan_services.planService.update_plan')
    def test_update_plan(self, mock_update_plan):
        # Mock the response from planService.update_plan
        mock_update_plan.return_value = {'id': 'mock_id', 'status': 'updated'}

        request_data = {'status': 'updated'}
        response = self.client.patch('/api/plan/mock_id', json=request_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'id': 'mock_id', 'status': 'updated'})

    @patch('src.services.plan_services.planService.update_plan', side_effect=Exception('Test error'))
    def test_update_plan_error(self, mock_update_plan):
        request_data = {'status': 'updated'}
        response = self.client.patch('/api/plan/mock_id', json=request_data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "A processing error occurred"})


if __name__ == '__main__':
    unittest.main()