# Python Automation Portfolio

Practical Python demo projects focused on small, clearly scoped automation and data tasks.

These projects are intentionally compact: each one demonstrates a workflow that can be adapted to real client requirements without claiming prior client work.

## Projects

| Project | What it demonstrates | Main tools |
|---|---|---|
| [CSV Data Cleaner](01-csv-data-cleaner/) | Data cleaning, normalization, deduplication, QA | Python, pandas |
| [Web Scraper to Excel](02-web-scraper-to-excel/) | HTML parsing, structured extraction, deduplication, Excel export | Python, requests, BeautifulSoup, pandas |
| [REST API / JSON to Excel](03-api-json-to-excel/) | REST API calls, nested JSON flattening, validation, Excel export | Python, requests, pandas |

## Typical Problems These Projects Map To

- Clean messy CSV or Excel data
- Remove duplicates and standardize fields
- Extract public website data into a spreadsheet
- Convert API / JSON responses into a clean table
- Automate repetitive data-processing steps
- Produce structured CSV / XLSX outputs with basic QA checks

## Run Locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Each project folder contains its own usage instructions and sample output.

## Notes

- All portfolio data is synthetic or comes from public demo/test sources.
- No private client data, credentials, or confidential work information is included.
- The focus is reproducible code, clear outputs, and practical QA.
