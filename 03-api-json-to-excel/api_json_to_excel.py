#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import pandas as pd
import requests

DEFAULT_URL = "https://jsonplaceholder.typicode.com/users"

def flatten_user(user, source):
    return {
        "id": user["id"],
        "name": user["name"],
        "username": user["username"],
        "email": user["email"].strip().lower(),
        "phone": user["phone"],
        "website": user["website"],
        "city": user["address"]["city"],
        "zipcode": user["address"]["zipcode"],
        "latitude": float(user["address"]["geo"]["lat"]),
        "longitude": float(user["address"]["geo"]["lng"]),
        "company": user["company"]["name"],
        "company_catchphrase": user["company"]["catchPhrase"],
        "source_url": source,
    }

def main():
    parser = argparse.ArgumentParser(description="Flatten REST API JSON into CSV/XLSX.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--json-file")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.json_file:
        data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        source = f"offline fixture: {Path(args.json_file).name}"
    else:
        response = requests.get(args.url, timeout=20)
        response.raise_for_status()
        data = response.json()
        source = args.url

    df = pd.DataFrame(flatten_user(user, source) for user in data)

    qa = {
        "records": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_emails": int(df["email"].isna().sum() + (df["email"] == "").sum()),
        "missing_companies": int(df["company"].isna().sum() + (df["company"] == "").sum()),
    }

    df.to_csv(output_dir / "api_users_flattened.csv", index=False)
    df.to_excel(output_dir / "api_users_flattened.xlsx", index=False)
    (output_dir / "qa_summary.json").write_text(
        json.dumps(qa, indent=2), encoding="utf-8"
    )
    print(json.dumps(qa, indent=2))

if __name__ == "__main__":
    main()
