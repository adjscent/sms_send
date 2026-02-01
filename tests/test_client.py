"""Unit tests for SMS Send module."""

import unittest
from unittest.mock import patch, MagicMock
from sms_send import SMSClient
import time


class TestSMSClient(unittest.TestCase):
    """Test cases for SMSClient."""
    
    def test_init_with_http(self):
        """Test client initialization with http URL."""
        client = SMSClient("http://192.168.1.100:8080")
        self.assertEqual(client.endpoint, "http://192.168.1.100:8080/sms/send")
    
    def test_init_without_http(self):
        """Test client initialization without http prefix."""
        client = SMSClient("192.168.1.100:8080")
        self.assertEqual(client.endpoint, "http://192.168.1.100:8080/sms/send")
    
    def test_init_with_https(self):
        """Test client initialization with https URL."""
        client = SMSClient("https://192.168.1.100:8080")
        self.assertEqual(client.endpoint, "https://192.168.1.100:8080/sms/send")
    
    @patch('sms_send.client.requests.post')
    def test_send_sms_without_sim_slot(self, mock_post):
        """Test sending SMS without SIM slot."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response
        
        # Create client and send SMS
        client = SMSClient("192.168.1.100:8080")
        result = client.send_sms(
            phone_numbers="15888888888",
            msg_content="Test message"
        )
        
        # Verify request was made
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check endpoint
        self.assertEqual(call_args[0][0], "http://192.168.1.100:8080/sms/send")
        
        # Check payload structure
        payload = call_args[1]['json']
        self.assertIn('data', payload)
        self.assertIn('timestamp', payload)
        self.assertIn('sign', payload)
        
        # Check data fields
        self.assertEqual(payload['data']['phone_numbers'], "15888888888")
        self.assertEqual(payload['data']['msg_content'], "Test message")
        self.assertNotIn('sim_slot', payload['data'])
        
        # Check result
        self.assertEqual(result, {"status": "success"})
    
    @patch('sms_send.client.requests.post')
    def test_send_sms_with_sim_slot(self, mock_post):
        """Test sending SMS with SIM slot."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response
        
        # Create client and send SMS
        client = SMSClient("192.168.1.100:8080")
        result = client.send_sms(
            phone_numbers="15888888888;19999999999",
            msg_content="Test message",
            sim_slot=1
        )
        
        # Check payload
        payload = mock_post.call_args[1]['json']
        self.assertEqual(payload['data']['sim_slot'], 1)
        self.assertEqual(payload['data']['phone_numbers'], "15888888888;19999999999")
    
    @patch('sms_send.client.requests.post')
    def test_send_sms_timestamp(self, mock_post):
        """Test that timestamp is generated correctly."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response
        
        # Create client and send SMS
        client = SMSClient("192.168.1.100:8080")
        before_time = int(time.time() * 1000)
        client.send_sms(
            phone_numbers="15888888888",
            msg_content="Test"
        )
        after_time = int(time.time() * 1000)
        
        # Check timestamp is within expected range
        payload = mock_post.call_args[1]['json']
        timestamp = payload['timestamp']
        self.assertGreaterEqual(timestamp, before_time)
        self.assertLessEqual(timestamp, after_time)


if __name__ == '__main__':
    unittest.main()
