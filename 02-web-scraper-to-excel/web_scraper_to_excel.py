#!/usr/bin/env python3
from pathlib import Path
import argparse
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://books.toscrape.com/catalogue/page-1.html"

def parse_catalog(html, source):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("article.product_pod"):
        title_el = card.select_one("h3 a")
        price_el = card.select_one(".price_color")
        stock_el = card.select_one(".availability")
        if not (title_el and price_el):
            continue

        title = title_el.get("title") or title_el.get_text(" ", strip=True)
        match = re.search(r"([0-9]+(?:\.[0-9]+)?)", price_el.get_text(" ", strip=True))
        rows.append({
            "product_name": title.strip(),
            "price_gbp": float(match.group(1)) if match else None,
            "availability": stock_el.get_text(" ", strip=True) if stock_el else "",
            "source_url": source,
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df["_key"] = df["product_name"].str.strip().str.casefold()
        df = df.drop_duplicates("_key").drop(columns="_key").reset_index(drop=True)
    return df

def main():
    parser = argparse.ArgumentParser(description="Extract product data to CSV/XLSX.")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--html-file")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.html_file:
        html = Path(args.html_file).read_text(encoding="utf-8")
        source = f"offline fixture: {Path(args.html_file).name}"
    else:
        response = requests.get(
            args.url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        html = response.text
        source = args.url

    df = parse_catalog(html, source)
    df.to_csv(output_dir / "scraped_products.csv", index=False)
    df.to_excel(output_dir / "scraped_products.xlsx", index=False)

    print(f"Exported {len(df)} unique products.")

if __name__ == "__main__":
    main()
