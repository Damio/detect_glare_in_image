import unittest
from camera_glare.app import app


import json

class MyAppCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_ping(self):
        response = self.app.get("/ping")
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(data['res'], "pong")

    def test_check_flare(self):
        response = self.app.post(
            "/detect_glare",
            json={
                "lat": 49.2699648, 
                "lon": -123.1290368, 
                "epoch": 1588704959.321, 
                "orientation": -10.2
                }
                ,)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'glare': False})
    
    # def test_check_flare_invalid_data(self):
    #     # Note: the lat is not within range, so we expect an error
    #     response = self.app.post(
    #         "/detect_glare",
    #         json={
    #             "lat": 94.33, 
    #             "lon": -123.1290368, 
    #             "epoch": 1588704959.321, 
    #             "orientation": -10.2
    #             }
    #             ,)
    #     self.assertEqual(response.status_code, 400)
        


if __name__ == '__main__':
    unittest.main()