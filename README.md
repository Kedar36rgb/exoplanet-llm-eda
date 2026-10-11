# Exoplanet Discovery Trends — LLM-assisted EDA

## What I asked
- How have exoplanet discoveries changed by year?
- Which discovery methods dominate?
- How complete is the radius and mass data?

## Data
- Source: Kaggle / NASA Exoplanet Archive
- Files used: `exoplanets_clean.csv` (main), `discovery_year_summary.csv`, `discovery_method_summary.csv`, `data_dictionary.csv`
- Rows after cleaning: 6,336
- Years covered: 1992 to 2026

## Method
1. Cleaned missing values in pandas and dropped the `source_publication_date` column (which was 100% empty).
2. Computed summary statistics (years, methods, radius, mass, habitable proxy).
3. Created 3 charts: discoveries per year, top methods, radius distribution.
4. Exported findings to `outputs/findings.json`.
5. Asked an LLM to turn ONLY that JSON into a draft narrative.
6. Manually verified every number in the summary against the JSON.

## Key findings (human-verified)
- A total of 6,336 planets were analyzed, discovered between 1992 and 2026.
- Transit is the most common discovery method (4,676 planets), followed by Radial Velocity (1,197) and Microlensing (282).
- The most common planet size class is Neptune-like (2,082), followed closely by Super-Jupiter (1,828) and Super-Earth (1,195).
- Most planets fall into the "Hot" (2,666) or "Warm" (2,334) temperature bands, with 61 identified as potentially habitable proxies.
- The year 2016 recorded the highest single-year discovery count with 1,504 planets.

## AI usage disclosure
- **Model:** GEMINI AI
- **Used for:** Drafting the narrative summary from my computed `findings.json`.
- **Not used for:** Data cleaning, statistics, chart creation, or choosing findings.
- **Verification:** Every number in the AI summary was checked against `outputs/findings.json`. I confirmed all numbers were accurate and made no edits.
- **Prompt:** See `outputs/summary_prompt.txt`
- **Raw AI output:** See `outputs/llm_summary_raw.md`

## Limitations
- Missing radius (0.8%) and mass (0.5%) values can bias the analysis.
- The AI correctly noted that the yearly breakdown only covers recent years (2012-2026) as computed.
- Discovery trends reflect telescope and survey activity, not only true planet frequency.
- LLM summaries can hallucinate; all numbers were verified.
- No causal claims are made.

## Reproduce
```bash
pip install -r requirements.txt
python src/analyze.py
python src/llm_summary.py
