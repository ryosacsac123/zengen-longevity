import unittest
import json
from app import app

class TestJDI8(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_perfect_score(self):
        # All positive items HIGH (True), Beef/Pork LOW (False)
        payload = {
            'rice': True,
            'miso_soup': True,
            'seaweed': True,
            'pickles': True,
            'green_yellow_veg': True,
            'fish': True,
            'green_tea': True,
            'beef_pork': False 
        }
        response = self.app.post('/api/calculate_score', json=payload)
        data = json.loads(response.data)
        self.assertEqual(data['score'], 8)
        self.assertIn('High (14% lower mortality risk)', data['risk_reduction'])

    def test_poor_score(self):
        # All positive items LOW (False), Beef/Pork HIGH (True)
        payload = {
            'rice': False,
            'miso_soup': False,
            'seaweed': False,
            'pickles': False,
            'green_yellow_veg': False,
            'fish': False,
            'green_tea': False,
            'beef_pork': True 
        }
        response = self.app.post('/api/calculate_score', json=payload)
        data = json.loads(response.data)
        self.assertEqual(data['score'], 0)

    def test_mixed_score(self):
        # 3 positives HIGH, Beef/Pork LOW (Good) -> 3 + 1 = 4
        payload = {
            'rice': True,
            'miso_soup': True,
            'seaweed': True,
            'pickles': False,
            'green_yellow_veg': False,
            'fish': False,
            'green_tea': False,
            'beef_pork': False 
        }
        response = self.app.post('/api/calculate_score', json=payload)
        data = json.loads(response.data)
        self.assertEqual(data['score'], 4)

if __name__ == '__main__':
    unittest.main()
