import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# Relevance scoring — tuned to David Renda (Senior Data Architect)
# Target skills: Azure Data Factory, Synapse, ADLS, Databricks, Snowflake,
#                dbt, Python, SQL, ELT/ETL, Power BI, Terraform, Bicep
# ---------------------------------------------------------------------------

SENIORITY_BOOST = {"senior", "sr.", "sr ", "staff", "principal", "lead", "head of", "director"}

def score_job(title: str) -> int:
    """Return 0-100 relevance score based on job title vs David's profile."""
    if not title:
        return 0
    t = title.lower()

    def has_seniority():
        return any(s in t for s in SENIORITY_BOOST)

    # ------------------------------------------------------------------
    # Tier 1 (90-100): Perfect match — Data Architect / Azure Architect
    # ------------------------------------------------------------------
    tier1 = [
        "data architect", "data platform architect", "cloud data architect",
        "enterprise data architect", "azure architect", "azure data architect",
        "analytics architect", "data infrastructure architect",
        "solutions architect, data", "data warehouse architect",
    ]
    for kw in tier1:
        if kw in t:
            return min(100, 92 + (5 if has_seniority() else 0))

    # ------------------------------------------------------------------
    # Tier 2 (70-89): Strong match — Data Engineer / Analytics Engineer
    # ------------------------------------------------------------------
    tier2 = [
        "data engineer", "analytics engineer", "azure data engineer",
        "data platform engineer", "cloud data engineer",
        "data infrastructure engineer", "etl architect", "pipeline architect",
        "solutions architect",  # general SA still very relevant
        "cloud architect",
    ]
    for kw in tier2:
        if kw in t:
            return min(100, 73 + (6 if has_seniority() else 0))

    # ------------------------------------------------------------------
    # Tier 3 (50-69): Good match — BI, DB, Cloud, ML adjacent
    # ------------------------------------------------------------------
    tier3_exact = [
        "bi engineer", "bi developer", "business intelligence engineer",
        "business intelligence developer", "etl developer", "etl engineer",
        "database engineer", "data warehouse engineer", "mlops engineer",
        "data reliability engineer",
    ]
    for kw in tier3_exact:
        if kw in t:
            return 62

    tier3_broad = [
        "business intelligence", "data analyst", "cloud engineer",
        "platform engineer", "database administrator", "dba",
        "machine learning engineer", "ml engineer", "machine learning",
        "data scientist",  # adjacent, not primary target
        "azure developer", "azure engineer",
        "snowflake", "databricks", "dbt developer",
    ]
    for kw in tier3_broad:
        if kw in t:
            return 55

    # ------------------------------------------------------------------
    # Tier 4 (25-49): Weak match — general tech
    # ------------------------------------------------------------------
    tier4 = [
        "software engineer", "backend engineer", "backend developer",
        "site reliability", "sre ", "devops", "platform",
        "security engineer", "network engineer", "systems engineer",
        "infrastructure engineer", "technical program manager",
        "engineering manager", "data product manager",
    ]
    for kw in tier4:
        if kw in t:
            return 30

    # ------------------------------------------------------------------
    # Default: not a match
    # ------------------------------------------------------------------
    return 8


# Load both datasets
greenhouse_df = pd.read_csv("all_jobs.csv")
sacramento_df = pd.read_csv("sacramento_jobs.csv")

print("="*70)
print("COMBINING JOB DATA")
print("="*70)

print(f"\nGreenhouse jobs: {len(greenhouse_df)}")
print(f"Sacramento jobs: {len(sacramento_df)}")

# Standardize column names
sacramento_df = sacramento_df.rename(columns={
    "scraped_at": "last_updated"
})

# Add location if not present
if "location" not in sacramento_df.columns:
    sacramento_df["location"] = "Sacramento, CA"

# Add source column
greenhouse_df["source"] = "Greenhouse"
sacramento_df["source"] = "Career Page"

# Add last_updated timestamp
if "last_updated" not in greenhouse_df.columns:
    greenhouse_df["last_updated"] = datetime.now().isoformat()

# Combine
combined_df = pd.concat([greenhouse_df, sacramento_df], ignore_index=True)

# Remove duplicates (same title + company + location)
combined_df_clean = combined_df.drop_duplicates(
    subset=["title", "company", "location"],
    keep="first"
)

print(f"\nCombined total: {len(combined_df_clean)}")
print(f"Duplicates removed: {len(combined_df) - len(combined_df_clean)}")

# Score each job for relevance
print("\nScoring jobs for relevance...")
combined_df_clean = combined_df_clean.copy()
combined_df_clean["relevance_score"] = combined_df_clean["title"].apply(score_job)

# Sort by score descending so the CSV is already ranked
combined_df_clean = combined_df_clean.sort_values("relevance_score", ascending=False)

# Save combined
combined_df_clean.to_csv("all_jobs_combined.csv", index=False)
print(f"\nSaved to all_jobs_combined.csv")

# Print score distribution
score_bins = [
    ("Excellent (90-100)", combined_df_clean["relevance_score"] >= 90),
    ("Strong   (70-89)",   (combined_df_clean["relevance_score"] >= 70) & (combined_df_clean["relevance_score"] < 90)),
    ("Good     (50-69)",   (combined_df_clean["relevance_score"] >= 50) & (combined_df_clean["relevance_score"] < 70)),
    ("Weak     (25-49)",   (combined_df_clean["relevance_score"] >= 25) & (combined_df_clean["relevance_score"] < 50)),
    ("Low      (0-24)",    combined_df_clean["relevance_score"] < 25),
]
print("\nRelevance score breakdown:")
for label, mask in score_bins:
    count = mask.sum()
    print(f"  {label}: {count:,} jobs")

# Show breakdown
print(f"\nBreakdown by source:")
print(combined_df_clean["source"].value_counts())

print(f"\nBreakdown by location (top 10):")
print(combined_df_clean["location"].value_counts().head(10))