import traceback
import os
import pytest
import requests
from datetime import datetime

from config.config import TEST_RESULTS_DIR,TEST_REPORTS_DIR
from utils.docx_generator.export_to_docx import export_all_results_to_docx
from utils.report_generator.generate_report import generate_html_report
from helper_functions.write_to_csv import update_csv_with_id
from helper_functions.csv_reader import get_combined_test_data

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
ENVIRONMENT = "SIT"
TESTER_NAME = "Harsha Maiya"

TEST_REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "test_reports", "test_report.html")

# ---------------- Pytest Context ---------------- #

@pytest.fixture(scope="session")
def test_context():
    """Shared context for storing results, auto-generates reports on teardown."""
    context = {
        "all_results": []
    }
    yield context  # tests can append to this

    # --- Teardown: generate reports ---
    generate_html_report(
        test_results=context["all_results"],
        environment=ENVIRONMENT,
        tester_name=TESTER_NAME,
        report_path = TEST_REPORT_PATH
    )

    export_all_results_to_docx(
        test_results=context["all_results"],
        output_dir=TEST_RESULTS_DIR
    )


# ---------------- API Runners ---------------- #

def run_post_request(row, post_status_code):
    payload = {
        "userId": int(row["userId"]),
        "title": row["title"],
        "body": row["body"]
    }
    response = requests.post(BASE_URL, json=payload)
    return {
        "result_heading": "POST/Users",
        "method": "POST",
        "url": response.url,
        "headers": dict(response.request.headers),
        "body": payload,
        "status_code": response.status_code,
        "response_headers": dict(response.headers),
        "response_body": response.json(),
        "assertions": [
            {
                "assertion": "Status Code - ",
                "expected": post_status_code,
                "actual": response.status_code,
                "result": response.status_code == post_status_code
            }
        ]
    }


def run_get_request(post_id, get_status_code):
    url = f"{BASE_URL}/{post_id}"
    response = requests.get(url,params=params, proxies=proxies, verify=False)
    return {
        "result_heading": "GET/Users",
        "method": "GET",
        "url": response.url,
        "headers": dict(response.request.headers),
        "body": None,
        "status_code": response.status_code,
        "response_headers": dict(response.headers),
        "response_body": response.json(),
        "assertions": [
            {
                "assertion": "Status Code - ",
                "expected": get_status_code,
                "actual": response.status_code,
                "result": response.status_code == get_status_code
            }
        ]
    }

# ---------------- Main Test ---------------- #

@pytest.mark.parametrize("row", get_combined_test_data())
def test_post_and_get(row, test_context):
    result = {
        "tc_no": row["tc_no"],
        "scenario": row["tc_name"],
        "description": row.get("tc_description", ""),
        "status": "Passed",
        "requests": []
    }

    try:
        # Run POST
        post_result = run_post_request(row, int(row['post_status_code']))
        result["requests"].append(post_result)

        post_id = post_result["response_body"].get("userId")
        post_id_csv = post_result["response_body"].get("id")

        # Write returned ID back to CSV
        if post_id:
            update_csv_with_id(row["tc_no"], post_id_csv)

        # Run GET
        get_result = run_get_request(post_id, int(row['get_status_code']))
        result["requests"].append(get_result)

        # Check assertions
        if not all(
            assertion["result"]
            for request in result["requests"]
            for assertion in request["assertions"]
        ):
            result["status"] = "Failed"

    except Exception as e:
        # Capture error info
        result["status"] = "Error"
        result["error_message"] = str(e)
        result["error_type"] = type(e).__name__
        result["error_traceback"] = traceback.format_exc()
        result["error_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    finally:
        test_context["all_results"].append(result)
