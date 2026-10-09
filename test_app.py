import unittest
import json
from app import app

class TestSchedulingAPI(unittest.TestCase):

    def setUp(self):
        # Maak een virtuele test-client van de Flask app
        self.client = app.test_client()

    def test_get_eligible_employees(self):
        """Test GET /shifts/:id/eligible-employees voor een open shift"""
        response = self.client.get('/shifts/s5/eligible-employees')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('eligible_employees', data)

    def test_assign_missing_skill(self):
        """Test POST /shifts/:id/assign met ontbrekende skill"""
        response = self.client.post('/shifts/s2/assign', json={"employee_id": "e2"})
        self.assertEqual(response.status_code, 400)

    def test_assign_overlap(self):
        """Test POST /shifts/:id/assign met tijdsoverlap"""
        response = self.client.post('/shifts/s2/assign', json={"employee_id": "e1"})
        self.assertEqual(response.status_code, 409)

if __name__ == '__main__':
    unittest.main()