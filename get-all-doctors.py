import json
import time
import requests

URL = "https://medre.tehik.ee/api-common/public/persons/filter"

payload = {
    "occupationCode": "",
    "firstName": "",
    "lastName": "",
    "occupation": "Arst",
    # "speciality": "E620", # If you need to filter by speciality
    "sort": None,
    "page": 0,
    "size": 50,
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}


def fetch_all_doctors():
    all_doctors = []
    current_page = 0
    total_pages = 1

    print("Starting API fetch...")

    while current_page < total_pages:
        payload["page"] = current_page
        print(f"Fetching page {current_page + 1}/{total_pages}...")

        try:
            response = requests.post(
                URL, json=payload, headers=headers, timeout=15
            )
            response.raise_for_status()
            data = response.json()

            # Update total pages from response metadata on page 0
            if current_page == 0:
                total_pages = data.get("totalPages", 1)
                total_elements = data.get("totalElements", 0)
                print(
                    f"Found {total_elements} total records across {total_pages} pages."
                )

            # Extract current page items and append to main list
            items = data.get("content", [])
            all_doctors.extend(items)

            current_page += 1

            # Respectful delay between API requests
            time.sleep(0.3)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {current_page}: {e}")
            break

    # Save aggregated output into a single JSON file
    output_filename = "all_medre_doctors.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(
            {
                "totalElements": len(all_doctors),
                # "totalPages": total_pages,
                "content": all_doctors,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(
        f"Finished! Successfully saved {len(all_doctors)} records to '{output_filename}'."
    )


if __name__ == "__main__":
    fetch_all_doctors()