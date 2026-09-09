import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SPLUNK_HEC_URL")
token = os.getenv("SPLUNK_HEC_TOKEN")

headers = {
    "Authorization": f"Splunk {token}"
}

payload = {
    "event": {
        "message": "Suricata HEC test",
        "test": True
    },
    "sourcetype": "_json",
    "index": "suricata",
    "host": "windows-hec-client"
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    verify=False,
    timeout=10
)

print("HTTP Status:", response.status_code)
print("Response:", response.text)