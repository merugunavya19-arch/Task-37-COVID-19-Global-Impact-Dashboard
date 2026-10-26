# COVID-19 Global Impact Dashboard

## Important notice
This package uses **synthetic practice data**, not official COVID-19 statistics. Country names are fictional labels and values were generated for software demonstration. Do not use the data for health, policy, clinical, or investment decisions.

## Contents
- `app.py`: interactive Streamlit dashboard with country/date filters, KPIs, Plotly trend charts and CSV download.
- `data/covid_synthetic_raw.csv`: generated source dataset.
- `data/covid_synthetic_clean.csv`: prepared dataset, including 7-day case average, case-fatality rate, and cautiously calculated doubling time.
- `clean_data.py`: repeatable cleaning and calculation pipeline.
- `reports/executive_summary.md` and `.pdf`: summary and dataset-derived observations.

## Dataset inspection
The generated dataset has 5 fictional country labels, daily observations from 2021-01-01 through 2022-12-31, and the eight requested source fields. It has 3,650 rows. Source values are generated complete and non-negative, with one row per country/date. The clean table adds three derived metrics. Vaccination coverage is deliberately not calculated because population denominators are not included.

## Run the dashboard
1. Install Python 3.10 or newer.
2. In a terminal, change to this folder.
3. Create a virtual environment (recommended): `python -m venv .venv` then activate it.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run: `streamlit run app.py`.
6. Open the local URL shown by Streamlit (usually http://localhost:8501). Use the sidebar to filter countries and dates.

## Rebuild cleaned data
Run `python clean_data.py` from this folder. The script validates required columns, parses dates and numeric values, removes duplicates, treats negative counts as missing, sorts records, and computes the derived fields.

## Presenting
Begin by stating the synthetic-data limitation. Demonstrate country/date filters, explain the difference between daily cases and cumulative totals, and mention that vaccination coverage is unavailable without population denominators. The dashboard reports selected-country cumulative KPIs as a sum of each country's latest available observation in the filtered date window.

