import os
import requests
import urllib3

from dotenv import load_dotenv

load_dotenv()

SPLUNK_HEC_URL = os.getenv("SPLUNK_HEC_URL")
SPLUNK_HEC_TOKEN = os.getenv("SPLUNK_HEC_TOKEN")

# Disable SSL warnings for this local lab.
# Do NOT use this approach in production.
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

def send_event(event):

    headers = {
        "Authorization": f"Splunk {SPLUNK_HEC_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "event": event,
        "sourcetype": "_json",
        "index": "suricata",
        "host": "windows-hec-client"
    }

    response = requests.post(
        SPLUNK_HEC_URL,
        headers=headers,
        json=payload,
        verify=False,
        timeout=10
    )

    if response.status_code != 200:

        print(
            "HEC error:",
            response.status_code,
            response.text
        )

        return False

    return True