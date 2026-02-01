"""Command-line interface for SMS Send."""

import argparse
import sys
from .client import SMSClient


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Send SMS via API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sms-send --server 192.168.1.100:8080 --phone 15888888888 --message "Hello"
  sms-send --server 192.168.1.100:8080 --phone "15888888888;19999999999" --message "Hello" --sim-slot 1
        """
    )
    
    parser.add_argument(
        '--server',
        required=True,
        help='Server address in format server_ip:port (e.g., 192.168.1.100:8080)'
    )
    
    parser.add_argument(
        '--phone',
        required=True,
        help='Phone number(s) - semicolon separated for multiple (e.g., "15888888888;19999999999")'
    )
    
    parser.add_argument(
        '--message',
        required=True,
        help='Message content to send'
    )
    
    parser.add_argument(
        '--sim-slot',
        type=int,
        choices=[1, 2],
        help='Optional SIM slot number (1 or 2)'
    )
    
    args = parser.parse_args()
    
    try:
        # Create client and send SMS
        client = SMSClient(args.server)
        result = client.send_sms(
            phone_numbers=args.phone,
            msg_content=args.message,
            sim_slot=args.sim_slot
        )
        
        print("SMS sent successfully!")
        print(f"Response: {result}")
        return 0
        
    except Exception as e:
        print(f"Error sending SMS: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
