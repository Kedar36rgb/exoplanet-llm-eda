import pandas as pd

df = pd.read_csv("data/raw/exoplanets_clean.csv", low_memory=False)

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values top 20:")
print(df.isna().mean().sort_values(ascending=False).head(20))