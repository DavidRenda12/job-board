import requests

# Test Lever
print("="*70)
print("TESTING LEVER API")
print("="*70)

lever_test = [
    {"name": "GitLab", "id": "gitlab"},
    {"name": "Plaid", "id": "plaid"},
    {"name": "Modal", "id": "modal"},
]

for company in lever_test:
    try:
        url = f"https://api.lever.co/v0/postings?mode=json&organization_id={company['id']}"
        print(f"\n{company['name']}:")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Jobs found: {len(data)}")
            if len(data) > 0:
                print(f"Sample: {data[0].get('text')[:50]}")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

# Test Workable
print("\n" + "="*70)
print("TESTING WORKABLE API")
print("="*70)

workable_test = [
    {"name": "Deel", "id": "deel"},
    {"name": "Twilio", "id": "twilio"},
    {"name": "Datadog", "id": "datadog"},
]

for company in workable_test:
    try:
        url = f"https://www.workable.com/api/v1/accounts/{company['id']}/jobs"
        print(f"\n{company['name']}:")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"Jobs found: {len(jobs)}")
            if len(jobs) > 0:
                print(f"Sample: {jobs[0].get('title')}")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")