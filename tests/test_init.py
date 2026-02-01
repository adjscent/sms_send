"""Test package initialization."""

import unittest
import sms_send


class TestInit(unittest.TestCase):
    """Test package initialization."""
    
    def test_version(self):
        """Test that version is defined."""
        self.assertTrue(hasattr(sms_send, '__version__'))
        self.assertIsInstance(sms_send.__version__, str)
    
    def test_sms_client_export(self):
        """Test that SMSClient is exported."""
        self.assertTrue(hasattr(sms_send, 'SMSClient'))
        self.assertIn('SMSClient', sms_send.__all__)


if __name__ == '__main__':
    unittest.main()
