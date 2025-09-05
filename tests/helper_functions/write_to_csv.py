import csv
import os
def update_csv_with_id(tc_no, post_id):
    """Update the CSV with the generated post_id for the given test case number."""
    # csv_file = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "input_files", "test_data.csv"))
    csv_file = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "input_files", "test_data.csv")
)

    rows = []
    with open(csv_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Ensure 'id' column exists
    if "id" not in fieldnames:
        fieldnames.append("id")

    # Update the correct row
    for row in rows:
        if row["tc_no"] == tc_no:  # Match test case number
            row["id"] = str(post_id)

    # Write back to CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
