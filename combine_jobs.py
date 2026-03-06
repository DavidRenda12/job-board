import pandas as pd
from datetime import datetime

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

# Save combined
combined_df_clean.to_csv("all_jobs_combined.csv", index=False)
print(f"\n✓ Saved to all_jobs_combined.csv")

# Show breakdown
print(f"\nBreakdown by source:")
print(combined_df_clean["source"].value_counts())

print(f"\nBreakdown by location (top 10):")
print(combined_df_clean["location"].value_counts().head(10))