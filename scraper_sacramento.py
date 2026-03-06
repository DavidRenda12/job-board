import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import json

# All 58 Sacramento companies to test
sacramento_companies = [
    ("Sutter Health", "https://jobs.sutterhealth.org"),
    ("UC Davis", "https://hr.ucdavis.edu/careers"),
    ("Recology", "https://recology.com/careers"),
    ("Kaiser Permanente", "https://careers.kaiserpermanente.org"),
    ("Wells Fargo", "https://careers.wellsfargo.com"),
    ("Bank of America", "https://careers.bankofamerica.com"),
    ("Raytheon", "https://careers.rtx.com"),
    ("Stryker", "https://careers.stryker.com"),
    ("Marriott", "https://careers.marriott.com"),
    ("Costco", "https://careers.costco.com"),
    ("Walmart", "https://careers.walmart.com"),
    ("Amazon", "https://amazon.jobs"),
    ("Microsoft", "https://careers.microsoft.com"),
    ("Google", "https://careers.google.com"),
    ("Apple", "https://jobs.apple.com"),
    ("Adobe", "https://careers.adobe.com"),
    ("IBM", "https://ibm.com/careers"),
    ("Cisco", "https://careers.cisco.com"),
    ("Intel", "https://jobs.intel.com"),
    ("Nvidia", "https://nvidia.com/careers"),
    ("DHL", "https://dhl.com/careers"),
    ("FedEx", "https://careers.fedex.com"),
    ("UPS", "https://jobs.ups.com"),
    ("Chase", "https://careers.jpmorgan.com"),
    ("Citibank", "https://citigroup.com/careers"),
    ("Fiserv", "https://careers.fiserv.com"),
    ("Accenture", "https://careers.accenture.com"),
    ("Capgemini", "https://capgemini.com/careers"),
    ("Cognizant", "https://careers.cognizant.com"),
    ("Infosys", "https://infosys.com/careers"),
    ("TCS", "https://tcs.com/careers"),
    ("Wipro", "https://wipro.com/careers"),
    ("GE", "https://gecareers.com"),
    ("Siemens", "https://siemens.com/careers"),
    ("3M", "https://3m.com/careers"),
    ("Caterpillar", "https://careers.caterpillar.com"),
    ("Tesla", "https://tesla.com/careers"),
    ("Lucid", "https://lucidmotors.com/careers"),
    ("Rivian", "https://rivian.com/careers"),
    ("Verizon", "https://verizon.com/careers"),
    ("AT&T", "https://att.com/careers"),
    ("T-Mobile", "https://t-mobile.com/careers"),
    ("Comcast", "https://comcast.com/careers"),
    ("Geico", "https://geico.com/careers"),
    ("State Farm", "https://statefarm.com/careers"),
    ("Progressive", "https://progressive.com/careers"),
    ("Zillow", "https://zillow.com/careers"),
    ("Redfin", "https://redfin.com/careers"),
    ("Opendoor", "https://opendoor.com/careers"),
    ("Whole Foods", "https://wholefoods.com/careers"),
    ("Home Depot", "https://homedepot.com/careers"),
    ("Lowes", "https://lowes.com/careers"),
    ("Sacramento Bee", "https://sacbee.com/careers"),
    ("Cal Fire", "https://fire.ca.gov/careers"),
    ("Sacramento County", "https://saccounty.net/careers"),
    ("City of Sacramento", "https://cityofsacramento.org/careers"),
    ("PG&E", "https://pge.com/careers"),
    ("SMUD", "https://smud.org/careers"),
]

def test_scrapability(url):
    """Test if a website has job listings"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text().lower()
        
        job_keywords = ['job', 'position', 'career', 'opening', 'hiring', 'apply', 'vacancy']
        return any(keyword in page_text for keyword in job_keywords)
    except:
        return False

def scrape_jobs(company_name, url):
    """Scrape jobs from a company career page"""
    jobs = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for job listings
        job_elements = soup.find_all(['div', 'li', 'article', 'a'], 
                                     class_=lambda x: x and any(keyword in x.lower() for keyword in ['job', 'position', 'opening']))
        
        for element in job_elements[:50]:
            title = element.get_text(strip=True)
            if len(title) > 5 and len(title) < 200:
                jobs.append({
                    "company": company_name,
                    "title": title[:150],
                    "url": url,
                    "scraped_at": datetime.now().isoformat(),
                })
        
        time.sleep(0.5)
    except Exception as e:
        pass
    
    return jobs

print("="*70)
print("AUTOMATED SACRAMENTO JOB SCRAPER")
print("="*70)

# Step 1: Test ALL 58 companies for scrapability
print(f"\nSTEP 1: Testing {len(sacramento_companies)} companies...\n")

scrapable_sites = []
not_scrapable = []

for i, (company_name, url) in enumerate(sacramento_companies):
    print(f"[{i+1}/{len(sacramento_companies)}] Testing {company_name}...", end=" ", flush=True)
    if test_scrapability(url):
        print("✓ SCRAPABLE")
        scrapable_sites.append((company_name, url))
    else:
        print("✗")
        not_scrapable.append(company_name)
    time.sleep(0.3)

print(f"\n{'='*70}")
print(f"Found {len(scrapable_sites)} scrapable sites out of {len(sacramento_companies)}")
print(f"Success rate: {100*len(scrapable_sites)//len(sacramento_companies)}%")

# Step 2: Scrape jobs from scrapable sites
print(f"\nSTEP 2: Scraping jobs from {len(scrapable_sites)} sites...\n")

all_jobs = []
for i, (company_name, url) in enumerate(scrapable_sites):
    print(f"[{i+1}/{len(scrapable_sites)}] Scraping {company_name}...", end=" ", flush=True)
    jobs = scrape_jobs(company_name, url)
    all_jobs.extend(jobs)
    print(f"✓ {len(jobs)} jobs")

# Step 3: Save with metadata
df = pd.DataFrame(all_jobs)

if len(df) > 0:
    # Remove duplicates
    df_clean = df.drop_duplicates(subset=["title", "company"], keep="first")
    
    # Add scrape timestamp for dashboard
    df_clean["scraped_at"] = datetime.now().isoformat()
    
    # Save CSV
    df_clean.to_csv("sacramento_jobs.csv", index=False)
    
    # Save metadata
    metadata = {
        "last_scraped": datetime.now().isoformat(),
        "total_jobs": len(df_clean),
        "companies_tested": len(sacramento_companies),
        "companies_scrapable": len(scrapable_sites),
        "success_rate": f"{100*len(scrapable_sites)//len(sacramento_companies)}%",
        "scrapable_sites": [name for name, url in scrapable_sites]
    }
    
    with open("scrape_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✓ Saved {len(df_clean)} jobs to sacramento_jobs.csv")
    print(f"✓ Saved metadata to scrape_metadata.json")
    print(f"Last scraped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nScrapable companies ({len(scrapable_sites)}):")
    for name, url in scrapable_sites:
        print(f"  ✓ {name}")
    
    if not_scrapable:
        print(f"\nNot scrapable ({len(not_scrapable)}):")
        for name in not_scrapable[:10]:
            print(f"  ✗ {name}")
        if len(not_scrapable) > 10:
            print(f"  ... and {len(not_scrapable) - 10} more")
else:
    print("❌ No jobs found")