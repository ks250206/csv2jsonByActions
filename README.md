## CSV to JSON by GitHub Actions

Simple helper script that converts CSV files under `data/` into JSON arrays under `output/`, keeping the same directory structure. Intended for running locally or from CI (e.g. GitHub Actions).

### Requirements
- Python 3.10+ (Actions uses 3.12)

### Usage
```bash
python scripts/csv_to_json.py data/sample.csv data/nested/list.csv
```
- Only `.csv` files under `data/` are processed.
- Converted files are written to `output/<original_path>.json`.
- CSVs are read as UTF-8; JSON is emitted with `ensure_ascii=False` so non-ASCII stays intact.

### Project structure
- `data/`: Source CSV files to convert.
- `output/`: Generated JSON files (created automatically).
- `scripts/csv_to_json.py`: Conversion script.

### Notes
- The script uses the first CSV row as headers via `csv.DictReader`.
- Non-CSV inputs are skipped with a warning.
