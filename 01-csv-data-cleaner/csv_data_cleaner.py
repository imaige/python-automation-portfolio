#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import pandas as pd

def clean_text(value):
    return "" if pd.isna(value) else re.sub(r"\s+", " ", str(value)).strip()

def normalize_phone(value):
    value = clean_text(value)
    if not value:
        return ""
    prefix = "+" if value.startswith("+") else ""
    return prefix + re.sub(r"\D", "", value)

def normalize_date(value):
    value = clean_text(value)
    if not value:
        return ""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return pd.to_datetime(value, format=fmt).strftime("%Y-%m-%d")
        except Exception:
            pass
    for fmt in ("%d-%m-%Y", "%d/%m/%Y"):
        try:
            return pd.to_datetime(value, format=fmt).strftime("%Y-%m-%d")
        except Exception:
            pass
    return ""

def clean_dataframe(df):
    required = {"name","email","phone","city","signup_date","status"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    before = len(df)
    out = df.copy()
    out["name"] = out["name"].map(lambda v: clean_text(v).title())
    out["email"] = out["email"].map(lambda v: clean_text(v).lower())
    out["phone"] = out["phone"].map(normalize_phone)
    out["city"] = out["city"].map(lambda v: clean_text(v).title())
    out["signup_date"] = out["signup_date"].map(normalize_date)
    out["status"] = out["status"].map(
        lambda v: {"active":"Active","inactive":"Inactive","pending":"Pending"}.get(
            clean_text(v).lower(), clean_text(v).title()
        )
    )
    out = out.drop_duplicates(subset=["email"], keep="first").reset_index(drop=True)

    summary = {
        "rows_before": before,
        "rows_after": len(out),
        "duplicates_removed": before - len(out),
        "blank_phones": int((out["phone"] == "").sum()),
        "blank_dates": int((out["signup_date"] == "").sum()),
    }
    return out, summary

def main():
    parser = argparse.ArgumentParser(description="Clean and deduplicate a contact CSV.")
    parser.add_argument("input_csv")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input_csv, dtype=str)
    cleaned, summary = clean_dataframe(df)

    cleaned.to_csv(output_dir / "cleaned_output.csv", index=False)
    cleaned.to_excel(output_dir / "cleaned_output.xlsx", index=False)
    (output_dir / "qa_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
