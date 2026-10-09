import json
import time
import requests

input_filename = "all_medre_doctors.json"
output_filename = "all_medre_doctors_detailed.json"
base_url = "https://medre.tehik.ee/api-common/public/persons/{id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    with open(input_filename, "r", encoding="utf-8") as f:
        doctors_list = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find '{input_filename}'.")
    exit(1)

doctors_list = doctors_list.get("content", [])
detailed_records = []

for index, doctor in enumerate(doctors_list, start=1):
    doctor_id = doctor.get("id")
    if not doctor_id:
        continue

    request_url = base_url.format(id=doctor_id)

    try:
        response = requests.get(request_url, headers=headers, timeout=10)
        response.raise_for_status()

        detail_data = response.json()
        detailed_records.append(detail_data)

        print(f"[{index}/{len(doctors_list)}] Fetched details for ID: {doctor_id}")

        time.sleep(0.2)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch details for ID {doctor_id}: {e}")

with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(detailed_records, f, ensure_ascii=False, indent=4)

print(f"\nDone! Saved {len(detailed_records)} detailed records to {output_filename}")