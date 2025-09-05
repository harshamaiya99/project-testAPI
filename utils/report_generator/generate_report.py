import json
import os
import webbrowser # Import the webbrowser module

def generate_html_report(test_results, environment, tester_name,report_path):
    total = len(test_results)
    passed = sum(1 for r in test_results if r["status"] == "Passed")
    failed = sum(1 for r in test_results if r["status"] == "Failed")
    error = sum(1 for r in test_results if r["status"] == "Error")
    pass_pct = (passed / total * 100) if total else 0

    css_path = os.path.join(os.path.dirname(__file__), "static", "style.css")
    js_path = os.path.join(os.path.dirname(__file__), "static", "script.js")
    template_path = os.path.join(os.path.dirname(__file__), "templates", "report_template.html")

    with open(css_path, "r", encoding="utf-8") as file:
        css_content = file.read()

    with open(js_path, "r", encoding="utf-8") as file:
        js_content = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        html_template = file.read()

    accordion_items = []
    for result in test_results:
        color = {"Passed": "green", "Failed": "red", "Error": "orange"}.get(result["status"], "gray")
        content_html = ""

        # Show error message if present (for Failed or Error)
        if "error_message" in result:
            content_html += (f"""
            <b>Error type: </b>{result["error_type"]}<br>
            <b>Error traceback: </b>{result["error_traceback"]}<br>
            <b>Error time: </b>{result["error_time"]}<br>
            <b>Error Message: </b> <div class='json-view-container'><pre class='json-view'>{result['error_message']}</pre><button class='copy-btn' title='Copy to clipboard'>📋</button></div><hr>
""")

        # Always show request/response/assertion details
        for i, req in enumerate(result["requests"], start=1):
            assertions_html = "".join(
                f"<li class='{'assertion-pass' if a['result'] else 'assertion-fail'}'>"
                f"{a['assertion']}: Expected {a['expected']}, Actual {a['actual']}</li>"
                for a in req['assertions']
            )

            content_html += f"""
            <b>Request {i} - {req['result_heading']}</b><br>
            Method: <b>{req['method']}</b><br>
            Endpoint URL: <b>{req['url']}</b><br>
            Request Headers: <div class='json-view-container'><pre class='json-view'>{json.dumps(req['headers'], indent=2)}</pre><button class='copy-btn' title='Copy to clipboard'>📋</button></div>
            {f"<b>Request Body:</b> <div class='json-view-container'><pre class='json-view'>{json.dumps(req['body'], indent=2)}</pre><button class='copy-btn' title='Copy to clipboard'>📋</button></div><br>" if req['body'] else ""}

            <hr>

            <b>Response Details</b><br>
            Status code: <b>{req['status_code']}</b><br>
            Response headers: <div class='json-view-container'><pre class='json-view'>{json.dumps(req['response_headers'], indent=2)}</pre><button class='copy-btn' title='Copy to clipboard'>📋</button></div>
            Response body: <div class='json-view-container'><pre class='json-view'>{json.dumps(req['response_body'], indent=2)}</pre><button class='copy-btn' title='Copy to clipboard'>📋</button></div>
            """

            if assertions_html:
                content_html += f"<hr><b>Assertions</b><ul>{assertions_html}</ul>"

            if i < len(result["requests"]):
                content_html += "<hr>"

        accordion_items.append(f"""
        <div class='accordion-item' data-status='{result['status']}'>
            <div class='accordion-header' onclick='toggleAccordion(this)'>
                <span>{result['tc_no']} {result['scenario']}</span>
                <span style='flex:1'></span>
                <span class='status' style='color:{color};'>&#9679; {result['status']}</span>
            </div>
            <div class='accordion-content'>
                {content_html}
            </div>
        </div>
        """)

    # format the dynamic content into the template, but leave CSS/JS as placeholders
    html_with_placeholders = html_template.format(
        total=total, passed=passed, failed=failed, error=error, pass_pct=pass_pct,
        environment=environment, tester_name=tester_name,
        accordion_html="\n".join(accordion_items)
    )

    # perform a simple string replace to inline the CSS and JS content
    html_output = html_with_placeholders.replace('<link rel="stylesheet" href="static/style.css">',
                                                 f'<style>{css_content}</style>')
    html_output = html_output.replace('<script src="static/script.js"></script>', f'<script>{js_content}</script>')

    # write everything to test_report.html file
    # html_path = os.path.join(os.path.dirname(__file__), "test_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    # --- Open the file in the default web browser ---
    webbrowser.open(f'file://{os.path.abspath(report_path)}')
