import os

# Root of the project
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Input test data
TEST_DATA_PATH = os.path.join(PROJECT_ROOT, "input_files", "test_data.csv")
TEST_CASE_PATH = os.path.join(PROJECT_ROOT, "input_files", "test_case.csv")

# Reports
TEST_REPORTS_DIR = os.path.join(PROJECT_ROOT, "test_reports")
HTML_REPORT = os.path.join(TEST_REPORTS_DIR, "test_report.html")

# Docx results
TEST_RESULTS_DIR = os.path.join(PROJECT_ROOT, "test_results")
DOCX_TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "utils", "docx_generator", "template.docx")
