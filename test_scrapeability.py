import requests
from bs4 import BeautifulSoup
import time

sacramento_companies = [
    ("Sutter Health", "jobs.sutterhealth.org"),
    ("UC Davis", "hr.ucdavis.edu/careers"),
    ("Recology", "recology.com/careers"),
    ("Kaiser Permanente", "careers.kaiserpermanente.org"),
    ("Wells Fargo", "careers.wellsfargo.com"),
    ("Bank of America", "careers.bankofamerica.com"),
    ("Raytheon", "careers.rtx.com"),
    ("Stryker", "careers.stryker.com"),
    ("Marriott", "careers.marriott.com"),
    ("Costco", "careers.costco.com"),
    ("Walmart", "careers.walmart.com"),
    ("Amazon", "amazon.jobs"),
    ("Microsoft", "careers.microsoft.com"),
    ("Google", "careers.google.com"),
    ("Apple", "jobs.apple.com"),
    ("Adobe", "careers.adobe.com"),
    ("IBM", "ibm.com/careers"),
    ("Cisco", "careers.cisco.com"),
    ("Intel", "jobs.intel.com"),
    ("Nvidia", "nvidia.com/careers"),
    ("DHL", "dhl.com/careers"),
    ("FedEx", "careers.fedex.com"),
    ("UPS", "jobs.ups.com"),
    ("Chase", "careers.jpmorgan.com"),
    ("Citibank", "citigroup.com/careers"),
    ("Fiserv", "careers.fiserv.com"),
    ("Accenture", "careers.accenture.com"),
    ("Capgemini", "capgemini.com/careers"),
    ("Cognizant", "careers.cognizant.com"),
    ("Infosys", "infosys.com/careers"),
    ("TCS", "tcs.com/careers"),
    ("Wipro", "wipro.com/careers"),
    ("GE", "gecareers.com"),
    ("Siemens", "siemens.com/careers"),
    ("3M", "3m.com/careers"),
    ("Caterpillar", "careers.caterpillar.com"),
    ("Tesla", "tesla.com/careers"),
    ("Lucid", "lucidmotors.com/careers"),
    ("Rivian", "rivian.com/careers"),
    ("Verizon", "verizon.com/careers"),
    ("AT&T", "att.com/careers"),
    ("T-Mobile", "t-mobile.com/careers"),
    ("Comcast", "comcast.com/careers"),
    ("Geico", "geico.com/careers"),
    ("State Farm", "statefarm.com/careers"),
    ("Progressive", "progressive.com/careers"),
    ("Zillow", "zillow.com/careers"),
    ("Redfin", "redfin.com/careers"),
    ("Opendoor", "opendoor.com/careers"),
    ("Whole Foods", "wholefoods.com/careers"),
    ("Home Depot", "homedepot.com/careers"),
    ("Lowes", "lowes.com/careers"),
    ("Sacramento Bee", "sacbee.com/careers"),
    ("Cal Fire", "fire.ca.gov/careers"),
    ("Sacramento County", "saccounty.net/careers"),
    ("City of Sacramento", "cityofsacramento.org/careers"),
    ("PG&E", "pge.com/careers"),
    ("SMUD", "smud.org/careers"),
]

print("="*70)
print("TESTING SACRAMENTO COMPANIES FOR SCRAPABLE CAREER PAGES")
print("="*70)

scrapable = []
not_scrapable = []
errors = []

for i, (company, domain) in enumerate(sacramento_companies):
    try:
        url = f"https://{domain}"
        print(f"[{i+1}/{len(sacramento_companies)}] {company}...", end=" ", flush=True)
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check if page has job listings (look for common job listing patterns)
            has_jobs = False
            job_keywords = ['job', 'position', 'career', 'opening', 'hiring', 'apply', 'vacancy']
            
            page_text = soup.get_text().lower()
            for keyword in job_keywords:
                if keyword in page_text:
                    has_jobs = True
                    break
            
            if has_jobs:
                print("✓ SCRAPABLE")
                scrapable.append((company, url))
            else:
                print("✗ No jobs found")
                not_scrapable.append((company, url))
        else:
            print(f"✗ Status {response.status_code}")
            not_scrapable.append((company, url))
        
        time.sleep(0.5)  # Be respectful to servers
    
    except requests.exceptions.Timeout:
        print("✗ Timeout")
        errors.append((company, "Timeout"))
    except Exception as e:
        print(f"✗ Error")
        errors.append((company, str(e)))

print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"\nSCRAPABLE ({len(scrapable)}):")
for company, url in scrapable:
    print(f"  ✓ {company}: {url}")

print(f"\nNOT SCRAPABLE ({len(not_scrapable)}):")
for company, url in not_scrapable[:10]:  # Show first 10
    print(f"  ✗ {company}")
if len(not_scrapable) > 10:
    print(f"  ... and {len(not_scrapable) - 10} more")

print(f"\nERRORS ({len(errors)}):")
for company, error in errors[:5]:  # Show first 5
    print(f"  ? {company}: {error}")
if len(errors) > 5:
    print(f"  ... and {len(errors) - 5} more")

print(f"\n{'='*70}")
print(f"Summary: {len(scrapable)} companies are scrapable")
print(f"Success rate: {len(scrapable)}/{len(sacramento_companies)} ({100*len(scrapable)//len(sacramento_companies)}%)")