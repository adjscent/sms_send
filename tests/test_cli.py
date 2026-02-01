"""Tests for CLI module."""

import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
from sms_send.cli import main


class TestCLI(unittest.TestCase):
    """Test cases for CLI."""
    
    @patch('sms_send.cli.SMSClient')
    @patch('sys.argv', ['sms-send', '--server', '192.168.1.100:8080', '--phone', '15888888888', '--message', 'Test'])
    def test_cli_basic(self, mock_client_class):
        """Test basic CLI usage."""
        # Setup mock
        mock_client = MagicMock()
        mock_client.send_sms.return_value = {"status": "success"}
        mock_client_class.return_value = mock_client
        
        # Run CLI
        result = main()
        
        # Verify client was created correctly
        mock_client_class.assert_called_once_with('192.168.1.100:8080')
        
        # Verify send_sms was called correctly
        mock_client.send_sms.assert_called_once_with(
            phone_numbers='15888888888',
            msg_content='Test',
            sim_slot=None
        )
        
        # Verify exit code
        self.assertEqual(result, 0)
    
    @patch('sms_send.cli.SMSClient')
    @patch('sys.argv', ['sms-send', '--server', '192.168.1.100:8080', '--phone', '15888888888;19999999999', '--message', 'Test', '--sim-slot', '1'])
    def test_cli_with_sim_slot(self, mock_client_class):
        """Test CLI with SIM slot."""
        # Setup mock
        mock_client = MagicMock()
        mock_client.send_sms.return_value = {"status": "success"}
        mock_client_class.return_value = mock_client
        
        # Run CLI
        result = main()
        
        # Verify send_sms was called with sim_slot
        mock_client.send_sms.assert_called_once_with(
            phone_numbers='15888888888;19999999999',
            msg_content='Test',
            sim_slot=1
        )
        
        self.assertEqual(result, 0)
    
    @patch('sms_send.cli.SMSClient')
    @patch('sys.argv', ['sms-send', '--server', '192.168.1.100:8080', '--phone', '15888888888', '--message', 'Test'])
    def test_cli_error_handling(self, mock_client_class):
        """Test CLI error handling."""
        # Setup mock to raise exception
        mock_client = MagicMock()
        mock_client.send_sms.side_effect = Exception("Connection error")
        mock_client_class.return_value = mock_client
        
        # Run CLI and capture stderr
        with patch('sys.stderr', new=StringIO()) as mock_stderr:
            result = main()
            stderr_output = mock_stderr.getvalue()
        
        # Verify error was printed and exit code is 1
        self.assertIn("Error sending SMS", stderr_output)
        self.assertIn("Connection error", stderr_output)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
