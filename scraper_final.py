import requests
import pandas as pd
import time

all_jobs = []

# GREENHOUSE - 50+ companies
greenhouse = [
    "stripe", "figma", "notion", "canva", "airbnb", "shopify", "databricks", 
    "retool", "linear", "cal", "plane", "counterpoint", "rippling", "deel",
    "brex", "mercury", "suno", "eleven-labs", "hugging-face", "anthropic",
    "openai", "replit", "cursor", "posthog", "cal-com", "supabase", "vercel",
    "netlify", "prisma", "tailwind", "next", "astro", "svelte", "solid",
    "remix", "nuxt", "fastapi", "django", "flask", "rust", "golang",
    "kubernetes", "docker", "hashicorp", "terraform", "pulumi", "aws",
    "azure", "gcp", "heroku", "railway", "render", "fly", "replit",
    "codecademy", "coursera", "udacity", "pluralsight", "linkedin-learning"
]

print("="*70)
print("SCRAPING GREENHOUSE JOBS (50+ companies)")
print("="*70)

for i, slug in enumerate(greenhouse):
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        print(f"[{i+1}/{len(greenhouse)}] {slug}...", end=" ", flush=True)
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get("jobs", [])
        print(f"✓ {len(jobs)}")
        
        for job in jobs:
            all_jobs.append({
                "company": slug,
                "ats": "Greenhouse",
                "title": job.get("title"),
                "location": job.get("location", {}).get("name"),
                "url": job.get("absolute_url"),
                "id": job.get("id"),
            })
        
        time.sleep(0.2)
    except Exception as e:
        print(f"✗")

# LEVER - 30+ companies
lever = [
    "lever", "gitlab", "guidepoint", "brighter", "catch", "cadence",
    "arc", "carta", "plaid", "mux", "sanity", "zenhub", "spacer",
    "vanta", "merge", "loom", "hume", "twelve-labs", "poolside",
    "magic", "together", "bittensor", "banana", "baseten", "baseten",
    "modal", "replicate", "huggingface", "openai", "anthropic"
]

print("\n" + "="*70)
print("SCRAPING LEVER JOBS (30+ companies)")
print("="*70)

for i, company_id in enumerate(lever):
    try:
        url = f"https://api.lever.co/v0/postings?mode=json&organization_id={company_id}"
        print(f"[{i+1}/{len(lever)}] {company_id}...", end=" ", flush=True)
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ {len(data)}")
        
        for job in data:
            location = None
            if job.get("locations"):
                location = job["locations"][0].get("name")
            
            all_jobs.append({
                "company": company_id,
                "ats": "Lever",
                "title": job.get("text"),
                "location": location,
                "url": job.get("hostedUrl"),
                "id": job.get("id"),
            })
        
        time.sleep(0.2)
    except Exception as e:
        print(f"✗")

# WORKABLE - 20+ companies
workable = [
    "workable", "deel", "spotify", "airbnb", "dropbox", "slack",
    "zoom", "figma", "notion", "stripe", "github", "gitlab",
    "heroku", "twilio", "sendgrid", "datadog", "elastic", "mongodb",
    "cockroach", "supabase"
]

print("\n" + "="*70)
print("SCRAPING WORKABLE JOBS (20+ companies)")
print("="*70)

for i, company_id in enumerate(workable):
    try:
        url = f"https://www.workable.com/api/v1/accounts/{company_id}/jobs"
        print(f"[{i+1}/{len(workable)}] {company_id}...", end=" ", flush=True)
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get("jobs", [])
        print(f"✓ {len(jobs)}")
        
        for job in jobs:
            location = None
            if job.get("location"):
                location = job["location"].get("name")
            
            all_jobs.append({
                "company": company_id,
                "ats": "Workable",
                "title": job.get("title"),
                "location": location,
                "url": job.get("url"),
                "id": job.get("id"),
            })
        
        time.sleep(0.2)
    except Exception as e:
        print(f"✗")

# Create DataFrame
df = pd.DataFrame(all_jobs)

# Remove duplicates (same title + location + company)
df_clean = df.drop_duplicates(subset=["title", "location", "company"], keep="first")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Raw jobs scraped: {len(df):,}")
print(f"After removing duplicates: {len(df_clean):,}")
print(f"Unique companies: {df_clean['company'].nunique()}")
print(f"By ATS Platform:")
for ats in df_clean["ats"].unique():
    count = len(df_clean[df_clean["ats"] == ats])
    print(f"  {ats}: {count:,} jobs")

# Save
df_clean.to_csv("all_jobs.csv", index=False)
print(f"\n✓ Saved {len(df_clean):,} jobs to all_jobs.csv")