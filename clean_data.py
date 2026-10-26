from pathlib import Path
import pandas as pd

EXPECTED = ["country", "date", "total_cases", "new_cases", "total_deaths", "new_deaths", "people_vaccinated", "people_fully_vaccinated"]

def clean_data(input_path, output_path):
    df = pd.read_csv(input_path)
    missing = [c for c in EXPECTED if c not in df.columns]
    if missing: raise ValueError(f"Missing required columns: {missing}")
    df = df[EXPECTED].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric = EXPECTED[2:]
    for c in numeric: df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["country", "date"]).drop_duplicates()
    # Invalid negative counts are treated as missing, not silently changed to zero.
    for c in numeric: df.loc[df[c] < 0, c] = pd.NA
    df = df.sort_values(["country", "date"]).reset_index(drop=True)
    df["cases_7d_avg"] = df.groupby("country")["new_cases"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    df["case_fatality_rate_pct"] = (df["total_deaths"] / df["total_cases"].where(df["total_cases"] > 0) * 100).where(df["total_cases"] > 0)
    # Doubling time only from two positive cumulative-case observations 7 days apart and growth > 0.
    def doubling(g):
        prev = g["total_cases"].shift(7)
        ratio = g["total_cases"] / prev.where(prev > 0)
        return (7 * 0.69314718056 / ratio.map(lambda r: __import__("math").log(r) if pd.notna(r) and r > 1 else float("nan"))).where(ratio > 1)
    df["case_doubling_time_days"] = df.groupby("country", group_keys=False).apply(doubling, include_groups=False).reset_index(level=0, drop=True) if False else pd.NA
    # Assign per-country calculation while retaining row alignment.
    for _, idx in df.groupby("country").groups.items():
        g = df.loc[idx]; prev = g["total_cases"].shift(7); ratio = g["total_cases"] / prev.where(prev > 0)
        import numpy as np
        valid = ratio > 1
        df.loc[idx, "case_doubling_time_days"] = (7*np.log(2)/np.log(ratio.where(valid))).to_numpy()
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    return df

if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    result = clean_data(base/"data/covid_synthetic_raw.csv", base/"data/covid_synthetic_clean.csv")
    print(f"Saved {len(result):,} rows; dates {result.date.min().date()} through {result.date.max().date()}; countries {result.country.nunique()}")
