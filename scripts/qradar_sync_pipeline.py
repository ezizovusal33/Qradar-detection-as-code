import os
import json
import requests
import urllib3

# Sertifikat xəbərdarlıqlarını gizlədirik
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub Secrets-dən məlumatları oxuyuruq
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
    
    print("QRadar-dakı mövcud qaydalar əldə edilir...")
    response = requests.get(base_url, headers=headers, verify=False)
    
    if response.status_code != 200:
        print(f"Xəta: Qaydalar çəkilə bilmədi. Status: {response.status_code}")
        return

    existing_rules = response.json()
    
    # Bütün qaydaları 'all_qradar_rules.json' faylına yazırıq
    with open('all_qradar_rules.json', 'w', encoding='utf-8') as f:
        json.dump(existing_rules, f, indent=4)
    print("Uğurlu! Bütün rule-lar 'all_qradar_rules.json' faylına yazıldı.")

    # GitHub-dakı JSON fayllarını oxuyub QRadar ilə sinxronizasiya edirik
    if os.path.exists(RULES_DIR):
        for filename in os.listdir(RULES_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(RULES_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    rule_data = json.load(f)
                
                rule_name = rule_data.get("name")
                rule_id = rule_data.get("id")
                
                if rule_id:
                    # Mövcud qayda üçün ID ilə POST sorğusu göndəririk (QRadar update üçün POST tələb edir)
                    update_url = f"{base_url}/{rule_id}"
                    print(f"'{rule_name}' qaydası ID ({rule_id}) ilə yenilənir (POST)...")
                    sync_res = requests.post(update_url, headers=headers, json=rule_data, verify=False)
                else:
                    # Yeni qayda üçün baza URL-ə POST sorğusu
                    print(f"'{rule_name}' yeni qayda olaraq yaradılır (POST)...")
                    sync_res = requests.post(base_url, headers=headers, json=rule_data, verify=False)
                
                if sync_res.status_code in [200, 201]:
                    print(f"Uğurlu! '{rule_name}' uğurla sinxronizasiya olundu.")
                else:
                    print(f"Sinxronizasiya xətası ({sync_res.status_code}): {sync_res.text}")

if __name__ == "__main__":
    sync_rules()
