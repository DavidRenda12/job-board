import requests
import pandas as pd
import time

# Define companies and their ATS platforms
greenhouse_companies = [
    {"name": "Stripe", "board_slug": "stripe"},
    {"name": "Figma", "board_slug": "figma"},
    {"name": "Notion", "board_slug": "notion"},
    {"name": "Canva", "board_slug": "canva"},
    {"name": "Airbnb", "board_slug": "airbnb"},
]

lever_companies = [
    {"name": "Lever", "company_id": "lever"},
    {"name": "GitLab", "company_id": "gitlab"},
    {"name": "Guidepoint", "company_id": "guidepoint"},
]

workable_companies = [
    {"name": "Workable", "company_id": "workable"},
    {"name": "Deel", "company_id": "deel"},
]

all_jobs = []
successful = 0
failed = 0

print("="*60)
print("SCRAPING GREENHOUSE JOBS")
print("="*60)

# Scrape Greenhouse
for i, company in enumerate(greenhouse_companies):
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company['board_slug']}/jobs"
        print(f"[{i+1}/{len(greenhouse_companies)}] {company['name']}...", end=" ")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        job_count = len(data.get("jobs", []))
        print(f"✓ {job_count} jobs")
        
        for job in data["jobs"]:
            job_record = {
                "company": company["name"],
                "ats_platform": "Greenhouse",
                "id": job.get("id"),
                "title": job.get("title"),
                "location": job.get("location", {}).get("name"),
                "url": job.get("absolute_url"),
            }
            all_jobs.append(job_record)
        
        successful += 1
        time.sleep(0.5)
    
    except Exception as e:
        print(f"✗ Error: {e}")
        failed += 1

print("\n" + "="*60)
print("SCRAPING LEVER JOBS")
print("="*60)

# Scrape Lever
for i, company in enumerate(lever_companies):
    try:
        url = f"https://api.lever.co/v0/postings?mode=json&organization_id={company['company_id']}"
        print(f"[{i+1}/{len(lever_companies)}] {company['name']}...", end=" ")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        job_count = len(data)
        print(f"✓ {job_count} jobs")
        
        for job in data:
            job_record = {
                "company": company["name"],
                "ats_platform": "Lever",
                "id": job.get("id"),
                "title": job.get("text"),
                "location": job.get("locations", [{}])[0].get("name") if job.get("locations") else None,
                "url": job.get("hostedUrl"),
            }
            all_jobs.append(job_record)
        
        successful += 1
        time.sleep(0.5)
    
    except Exception as e:
        print(f"✗ Error: {e}")
        failed += 1

print("\n" + "="*60)
print("SCRAPING WORKABLE JOBS")
print("="*60)

# Scrape Workable
for i, company in enumerate(workable_companies):
    try:
        url = f"https://www.workable.com/api/v1/accounts/{company['company_id']}/jobs"
        print(f"[{i+1}/{len(workable_companies)}] {company['name']}...", end=" ")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        job_count = len(data.get("jobs", []))
        print(f"✓ {job_count} jobs")
        
        for job in data.get("jobs", []):
            job_record = {
                "company": company["name"],
                "ats_platform": "Workable",
                "id": job.get("id"),
                "title": job.get("title"),
                "location": job.get("location", {}).get("name") if job.get("location") else None,
                "url": job.get("url"),
            }
            all_jobs.append(job_record)
        
        successful += 1
        time.sleep(0.5)
    
    except Exception as e:
        print(f"✗ Error: {e}")
        failed += 1

# Create DataFrame
df = pd.DataFrame(all_jobs)

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Successfully scraped: {successful} companies")
print(f"Failed: {failed} companies")
print(f"Total jobs: {len(df)}")
print(f"By ATS Platform:")
for platform in df["ats_platform"].unique():
    count = len(df[df["ats_platform"] == platform])
    print(f"  - {platform}: {count} jobs")

# Save to CSV
df.to_csv("all_jobs.csv", index=False)
print("\n✓ Saved to all_jobs.csv")
