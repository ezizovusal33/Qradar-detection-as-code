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
    # QRadar Offense Rules API endpoint (versiyaya gore /api/analytics/rules altindadir)
    base_url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    if not os.path.exists(RULES_DIR):
        print(f"Qovluq tapilmadi: {RULES_DIR}")
        return

    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(RULES_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    rule_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"JSON oxunma xətası ({filename}): {e}")
                continue
            
            rule_name = rule_data.get('name', filename)
            print(f"Yoxlanılır / Göndərilir: {rule_name}...")
            
            response = requests.post(base_url, headers=headers, json=rule_data, verify=False)
            
            if response.status_code in [200, 201]:
                print(f"Uğurlu! Qayda yaradıldı: {rule_name}")
            else:
                print(f"Sinxronizasiya xətası ({response.status_code}): {response.text}")

if __name__ == "__main__":
    sync_rules()
