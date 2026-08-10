# REST API / JSON to Excel

A compact API automation demo that fetches nested JSON, flattens it into a tabular structure, validates key fields, and exports CSV/XLSX output.

The live example uses the public JSONPlaceholder `/users` endpoint. A local sample JSON file is included for reproducible offline testing.

## Demonstrates

- REST API requests
- JSON parsing
- nested-object flattening
- type conversion
- field normalization
- CSV and XLSX export
- basic QA summary

## Run Offline

```bash
python api_json_to_excel.py --json-file sample_users.json
```

## Run Against the Public Test API

```bash
python api_json_to_excel.py
```

Output is written to `output/`.
