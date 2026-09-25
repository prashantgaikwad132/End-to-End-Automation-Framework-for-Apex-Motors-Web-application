"""
Data-Driven Testing (DDT) utilities — JSON and Excel loaders
"""

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(filename: str) -> dict[str, Any]:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def load_json_params(filename: str, key: str) -> list[dict]:
    """Load a list of param dicts for @pytest.mark.parametrize."""
    data = load_json(filename)
    return data.get(key, [])


def load_excel(filename: str, sheet_name: str = "Sheet1") -> list[dict]:
    """Load rows from an Excel sheet as list of dicts."""
    try:
        import openpyxl
    except ImportError:
        raise ImportError("openpyxl is required: pip install openpyxl")
    wb = openpyxl.load_workbook(DATA_DIR / filename, read_only=True, data_only=True)
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    headers = [str(h).strip() for h in rows[0]]
    return [dict(zip(headers, row)) for row in rows[1:]]
