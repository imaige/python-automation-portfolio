# Web Scraper to Excel

A small web-data extraction demo that parses structured product information and exports clean CSV/XLSX output.

The live example uses `books.toscrape.com`, a public scraping sandbox. An offline HTML fixture is also included so the project can be reproduced without a network request.

## Demonstrates

- HTTP requests
- HTML parsing with BeautifulSoup
- CSS selectors
- price extraction
- deduplication
- CSV and XLSX export

## Run Offline

```bash
python web_scraper_to_excel.py --html-file sample_catalog.html
```

## Run Against the Public Demo Site

```bash
python web_scraper_to_excel.py
```

Output is written to `output/`.
