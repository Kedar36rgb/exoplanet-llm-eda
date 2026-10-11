import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Setup paths
DATA = Path("data/raw/exoplanets_clean.csv")
OUT = Path("outputs")
CHARTS = OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA, low_memory=False)

# 1. Clean data
# Drop columns that are 100% empty
if "source_publication_date" in df.columns:
    df = df.drop(columns=["source_publication_date"])

# Drop rows without a discovery year or method
df = df.dropna(subset=["discovery_year", "discovery_method"]).copy()
df["discovery_year"] = df["discovery_year"].astype(int)

# Helper to safely count True values in the habitable proxy column
def count_true(series):
    return int(series.astype(str).str.lower().eq("true").sum())

# 2. Compute Findings
findings = {
    "n_planets": int(len(df)),
    "year_min": int(df["discovery_year"].min()),
    "year_max": int(df["discovery_year"].max()),
    "discoveries_by_year_recent": df["discovery_year"].value_counts().sort_index().tail(15).to_dict(),
    "top_discovery_methods": df["discovery_method"].value_counts().head(10).to_dict(),
    "median_radius_earth": round(float(df["radius_earth"].median()), 2) if "radius_earth" in df else None,
    "missing_radius_pct": round(float(df["radius_earth"].isna().mean() * 100), 1) if "radius_earth" in df else None,
    "median_mass_earth": round(float(df["mass_earth"].median()), 2) if "mass_earth" in df else None,
    "missing_mass_pct": round(float(df["mass_earth"].isna().mean() * 100), 1) if "mass_earth" in df else None,
    "habitable_proxy_count": count_true(df["potentially_habitable_proxy"]) if "potentially_habitable_proxy" in df else None,
    "planet_size_class_counts": df["planet_size_class"].value_counts().to_dict() if "planet_size_class" in df else {},
    "temperature_band_counts": df["temperature_band"].value_counts().to_dict() if "temperature_band" in df else {},
    "distance_band_counts": df["distance_band"].value_counts().to_dict() if "distance_band" in df else {},
}

# Save findings to JSON
with open(OUT / "findings.json", "w") as f:
    json.dump(findings, f, indent=2)

# 3. Create Charts
# Chart A: Discoveries per year
year_counts = df["discovery_year"].value_counts().sort_index()
plt.figure(figsize=(12, 5))
plt.plot(year_counts.index, year_counts.values, marker="o", color="navy")
plt.title("Exoplanets Discovered per Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(CHARTS / "discoveries_per_year.png", dpi=150)
plt.close()

# Chart B: Top methods
method_counts = df["discovery_method"].value_counts().head(10)
plt.figure(figsize=(10, 6))
method_counts.sort_values().plot(kind="barh", color="teal")
plt.title("Top 10 Discovery Methods")
plt.xlabel("Count")
plt.tight_layout()
plt.savefig(CHARTS / "top_methods.png", dpi=150)
plt.close()

# Chart C: Radius distribution
if "radius_earth" in df.columns:
    plt.figure(figsize=(10, 6))
    df["radius_earth"].dropna().clip(upper=30).hist(bins=50, color="coral")
    plt.title("Planet Radius Distribution (Clipped at 30 Earth Radii)")
    plt.xlabel("Radius (Earth radii)")
    plt.ylabel("Count")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / "radius_distribution.png", dpi=150)
    plt.close()

print("Done! Findings saved to outputs/findings.json and charts saved to outputs/charts/")