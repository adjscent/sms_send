# SMS Send

A Python module for sending SMS messages via API. Compatible with Windows and macOS.

## Installation

You can install the package using pip:

```bash
pip install .
```

Or install in development mode:

```bash
pip install -e .
```

## Usage

### Command Line Interface

After installation, you can use the `sms-send` command:

```bash
# Send SMS to a single number
sms-send --server 192.168.1.100:8080 --phone 15888888888 --message "Hello World"

# Send SMS to multiple numbers (semicolon-separated)
sms-send --server 192.168.1.100:8080 --phone "15888888888;19999999999" --message "Hello World"

# Specify SIM slot (optional)
sms-send --server 192.168.1.100:8080 --phone 15888888888 --message "Hello World" --sim-slot 1
```

### Python API

You can also use the module in your Python code:

```python
from sms_send import SMSClient

# Initialize client
client = SMSClient("192.168.1.100:8080")

# Send SMS
result = client.send_sms(
    phone_numbers="15888888888;19999999999",
    msg_content="Hello World",
    sim_slot=1  # Optional
)

print(result)
```

## API Details

The module sends requests to the endpoint: `server_ip:port/sms/send`

### Request Format

```json
{
  "data": {
    "sim_slot": 1,
    "phone_numbers": "15888888888;19999999999",
    "msg_content": "contents"
  },
  "timestamp": 1652590258638,
  "sign": ""
}
```

### Parameters

- `server_ip:port` (required): The server address and port
- `phone_numbers` (required): Semicolon-separated phone numbers
- `msg_content` (required): Message content to send
- `sim_slot` (optional): SIM card slot number (1 or 2)

## Requirements

- Python 3.7 or higher
- requests library (automatically installed)

## License

MIT License