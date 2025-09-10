import requests, csv, json, os, time

RAPDIAPI_key = open("RAPID_API_KEY").read().strip()

API_URL = "https://linkedin-scraper-api-real-time-fast-affordable.p.rapidapi.com/profile/detail"
API_HEADERS = {
    "x-rapidapi-host": "linkedin-scraper-api-real-time-fast-affordable.p.rapidapi.com",
    "x-rapidapi-key": RAPDIAPI_key
}

INPUT_FILE = "linkedin_profiles.csv"
OUTPUT_JSON = "linkedin_profiles_data.json"
OUTPUT_CSV = "linkedin_profiles_with_json.csv"

def load_profiles(csv_file, limit=10):
    profiles = []
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            profiles.append(row)
    return profiles

def fetch_profile(username):
    url = f"{API_URL}?username={username}"
    response = requests.get(url, headers=API_HEADERS, timeout=30)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed for {username}, status {response.status_code}")
        return None

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON saved: {filename}")

def save_csv(profiles, filename, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)
    print(f"CSV saved: {filename}")

# Currently the limit is set as 10 to fetch 10 profile
def main():
    profiles = load_profiles(INPUT_FILE, limit=10)
    print(f"Loaded {len(profiles)} profiles")

    results = {}
    enriched_profiles = []

    for row in profiles:
        username = row["username"]
        print(f"Fetching {username}...")
        profile_data = fetch_profile(username)

        if profile_data:
            # Save JSON result in dict
            results[username] = profile_data
            row["json"] = json.dumps(profile_data.get("data", profile_data))
            enriched_profiles.append(row)

        # Checkpoint saves
        save_json(results, OUTPUT_JSON)
        if enriched_profiles:
            save_csv(enriched_profiles, OUTPUT_CSV, fieldnames=list(row.keys()))

        time.sleep(2) 

    print("\n Finished fetching profiles.")

if __name__ == "__main__":
    main()