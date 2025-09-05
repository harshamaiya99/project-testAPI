import csv

# ---------------- CSV Readers ---------------- #
from config.config import TEST_CASE_PATH,TEST_DATA_PATH

def read_test_cases():
    """Read test case metadata (high-level info)."""
    with open(TEST_CASE_PATH, newline="", encoding="utf-8") as f:
        return {row["tc_no"]: row for row in csv.DictReader(f)}

def read_test_data():
    """Read actual test data (API payloads, expected status)."""
    with open(TEST_DATA_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def get_combined_test_data():
    """Merge test_cases + test_data by 'no'."""
    cases = read_test_cases()
    data = read_test_data()
    combined = []
    for row in data:
        tc_info = cases.get(row["tc_no"], {})
        combined.append({**tc_info, **row})  # merge dicts
    return combined