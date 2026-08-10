# CSV Data Cleaner

A compact Python utility for cleaning inconsistent contact data and producing validated spreadsheet output.

## Demonstrates

- whitespace cleanup
- name/city/status normalization
- email normalization
- phone normalization
- explicit date standardization
- duplicate removal by normalized email
- CSV and XLSX output
- JSON QA summary

## Run

```bash
python csv_data_cleaner.py sample_input.csv
```

Output is written to `output/`.

## Demo Result

- 20 input rows
- 17 unique output rows
- 3 duplicates removed

The sample data is synthetic.
