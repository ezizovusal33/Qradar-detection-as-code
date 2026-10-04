import os
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.environ.get("QRADAR_IP")
TOKEN = os.environ.get("QRADAR_TOKEN")

headers = {
    'SEC': TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

RULES_DIR = "qradar/rules"

def sync_rules():
    base_url = f"https://{QRADAR_IP}/api/analytics/rules"
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RULES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                rule_data = json.load(f)
            
            print(f"Syncing rule: {rule_data.get('name')}...")
            response = requests.post(base_url, headers=headers, json=rule_data, verify=False)
            print(f"Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    sync_rules()
