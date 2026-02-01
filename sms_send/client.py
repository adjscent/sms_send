"""SMS API Client for sending messages."""

import time
import requests
from requests.adapters import HTTPAdapter, Retry
from typing import Optional


class SMSClient:
    """Client for sending SMS via the API."""

    DEFAULT_TIMEOUT = 5  # seconds

    def __init__(self, server_url: str, timeout: Optional[float] = None, max_retries: int = 10, backoff_factor: float = 0.3):
        """
        Initialize SMS client.

        Args:
            server_url: Server URL in format 'server_ip:port' or 'http://server_ip:port'
            timeout: Default timeout for requests (seconds)
            max_retries: Number of retries for failed requests
            backoff_factor: Backoff factor for retries
        """
        if not server_url.startswith(('http://', 'https://')):
            server_url = f'http://{server_url}'

        self.server_url = server_url.rstrip('/')
        self.endpoint = f'{self.server_url}/sms/send'
        self.timeout = timeout or self.DEFAULT_TIMEOUT

        # Set up a session with retries
        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
    
    def send_sms(
        self,
        phone_numbers: str,
        msg_content: str,
        sim_slot: Optional[int] = None
    ) -> dict:
        """
        Send SMS to one or more phone numbers.

        Args:
            phone_numbers: Semicolon-separated phone numbers (e.g., "15888888888;19999999999")
            msg_content: Message content to send
            sim_slot: Optional SIM slot number (1 or 2)

        Returns:
            Response from the API as a dictionary

        Raises:
            requests.RequestException: If the API request fails
        """
        # Build request payload
        data = {
            "phone_numbers": phone_numbers,
            "msg_content": msg_content
        }

        # Add sim_slot only if provided
        if sim_slot is not None:
            data["sim_slot"] = sim_slot

        payload = {
            "data": data,
            "timestamp": int(time.time() * 1000),
            "sign": ""
        }

        # Make API request with timeout and retry
        response = self.session.post(self.endpoint, json=payload, timeout=self.timeout)
        response.raise_for_status()

        return response.json()
