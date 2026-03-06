import requests
import pandas as pd
import time
from itertools import product
import string

all_jobs = []

# GREENHOUSE - Expanded list (150+ companies)
greenhouse = [
    # Tier 1 Tech
    "stripe", "figma", "notion", "canva", "airbnb", "shopify", "databricks", 
    "retool", "linear", "cal", "plane", "counterpoint", "rippling", "deel",
    "brex", "mercury", "suno", "eleven-labs", "anthropic", "openai", "replit",
    "cursor", "posthog", "supabase", "vercel", "netlify", "prisma", "tailwind",
    
    # Developer Tools & Infrastructure
    "github", "gitlab", "hashicorp", "terraform", "pulumi", "docker",
    "kubernetes", "aws", "gcp", "azure", "heroku", "railway", "render",
    "fly", "codecademy", "coursera", "udacity", "pluralsight", "egghead",
    "frontendmasters", "scrimba", "nextjs", "nuxtjs", "remix",
    
    # Finance & Payments
    "chime", "revolut", "wise", "guidepoint", "carta", "plaid",
    "mux", "sanity", "vanta", "merge", "loom", "hume", "spacer",
    "together", "brighter", "cadence", "catch", "zenhub", "getgo",
    
    # Healthcare
    "ro", "teladoc", "livongo", "omada", "ginger", "talkspace",
    "betterhelp", "wyzant", "chegg", "coursehero", "skillshare",
    
    # Logistics & Supply Chain
    "flexport", "komodo", "turvo", "shippify", "loadwise", "getgo",
    
    # Real Estate
    "zillow", "redfin", "opendoor", "offerpad", "iproperty",
    
    # Food & Delivery
    "doordash", "gopuff", "instacart", "getir", "bukalapak",
    
    # Fintech
    "chasing", "clearco", "lemonade", "root", "hippo", "getgo",
    
    # Marketplace
    "shopee", "tokopedia", "lazada", "flipkart", "snapdeal",
    
    # Travel
    "klook", "agoda", "traveloka", "busuu", "duolingo",
    
    # Hardware/Robotics
    "anduril", "sanctuary", "carbon", "formlabs", "getgo",
    
    # AI/ML
    "huggingface", "replicate", "modal", "baseten", "banana",
    "poolside", "magic", "bittensor", "getgo",
    
    # Entertainment
    "spotify", "netflix", "hulu", "discord", "twitch", "getgo",
    
    # Social
    "snap", "pinterest", "nextdoor", "getgo",
    
    # Enterprise SaaS
    "calendly", "zendesk", "intercom", "hubspot", "salesforce",
    "slack", "zoom", "asana", "monday", "jira", "confluence",
    "trello", "getgo",
    
    # Security & Auth
    "okta", "auth0", "twilio", "sendgrid", "getgo",
    
    # Web Builders
    "wix", "squarespace", "webflow", "framer", "getgo",
    
    # Additional Companies
    "component", "algolia", "segment", "mobileye", "wiz",
    "snyk", "aqua", "sysdig", "lacework", "getgo",
    "notion-labs", "supabase-io", "vercel-app",
    
    # More startups
    "rippling-app", "brex-app", "mercury-bank", "suno-ai",
    "anthropic-ai", "openai-research", "replit-com",
]

# Remove duplicates and empty strings
greenhouse = [g.strip() for g in list(dict.fromkeys(greenhouse)) if g.strip()]

print("="*70)
print(f"SCRAPING GREENHOUSE JOBS ({len(greenhouse)} companies)")
print("="*70)

successful = 0
failed = 0
total_jobs_before_dedup = 0

for i, slug in enumerate(greenhouse):
    try:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
        print(f"[{i+1}/{len(greenhouse)}] {slug}...", end=" ", flush=True)
        
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get("jobs", [])
        print(f"✓ {len(jobs)}")
        
        total_jobs_before_dedup += len(jobs)
        
        for job in jobs:
            all_jobs.append({
                "company": slug,
                "ats": "Greenhouse",
                "title": job.get("title"),
                "location": job.get("location", {}).get("name"),
                "department": job.get("department", {}).get("name"),
                "url": job.get("absolute_url"),
                "id": job.get("id"),
            })
        
        if len(jobs) > 0:
            successful += 1
        
        time.sleep(0.15)
    except Exception as e:
        failed += 1
        print(f"✗")

# Create DataFrame
df = pd.DataFrame(all_jobs)

# Remove duplicates (same title + location + company)
df_clean = df.drop_duplicates(subset=["title", "location", "company"], keep="first")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Companies attempted: {len(greenhouse)}")
print(f"Companies with active jobs: {successful}")
print(f"Raw jobs scraped: {total_jobs_before_dedup:,}")
print(f"After removing duplicates: {len(df_clean):,}")
print(f"Unique companies with jobs: {df_clean['company'].nunique()}")
print(f"\nJobs removed as duplicates: {total_jobs_before_dedup - len(df_clean):,}")

# Save
df_clean.to_csv("all_jobs.csv", index=False)
file_size_mb = len(df_clean) * 0.001
print(f"\n✓ Saved {len(df_clean):,} jobs to all_jobs.csv")
print(f"File size: ~{file_size_mb:.1f} MB")