import unittest
from unittest.mock import Mock, patch
from api import APIEngine

class TestAPIEngine(unittest.TestCase):
    def setUp(self):
        self.api_engine = APIEngine()
        self.mock_credentials = {
            'api_key': 'test_key',
            'api_secret': 'test_secret'
        }

    @patch('requests.Session')
    @patch('requests.post')
    def test_broker_connection(self, mock_post, mock_session):
        # Test Dhan connection
        result = self.api_engine.connect_broker('dhan', self.mock_credentials)
        self.assertTrue(result)
        self.assertIn('dhan', self.api_engine.api_keys)

        # Test Angel One connection
        result = self.api_engine.connect_broker('angelone', self.mock_credentials)
        self.assertTrue(result)
        self.assertIn('angelone', self.api_engine.api_keys)

    @patch('requests.post')
    def test_trade_execution(self, mock_post):
        # Setup mock response
        mock_post.return_value.json.return_value = {'status': 'success', 'order_id': '123'}
        
        # Connect broker first
        self.api_engine.connect_broker('dhan', self.mock_credentials)
        
        # Test buy order
        result = self.api_engine.execute_trade(
            broker='dhan',
            symbol='TCS',
            order_type='BUY',
            quantity=1,
            price=3500.0
        )
        self.assertEqual(result['status'], 'success')

    @patch('websocket.WebSocketApp')
    def test_data_streaming(self, mock_ws):
        def mock_callback(data):
            pass

        # Test websocket stream initialization
        self.api_engine.connect_broker('dhan', self.mock_credentials)
        self.api_engine.stream_data('dhan', ['TCS', 'INFY'], mock_callback)
        mock_ws.assert_called_once()

    def test_signature_generation(self):
        timestamp = "1234567890"
        signature = self.api_engine._generate_signature(
            self.mock_credentials['api_secret'],
            timestamp
        )
        self.assertTrue(isinstance(signature, str))
        self.assertTrue(len(signature) > 0)

    def test_header_generation(self):
        self.api_engine.api_keys['dhan'] = self.mock_credentials
        headers = self.api_engine._get_dhan_headers()
        
        self.assertIn('X-Auth-Token', headers)
        self.assertIn('X-Auth-Signature', headers)
        self.assertIn('X-Auth-Timestamp', headers)

def run_api_tests():
    print("Starting API Integration Tests...")
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == "__main__":
    run_api_tests()
