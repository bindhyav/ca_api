import pytest
import datetime
import os
from utils import get_focused_app,get_selected_device,get_product_details, get_serial_number


def run_tests():
    # Remove JAVA_HOME from environment if it exists
    global mode
    os.environ.pop("JAVA_HOME", None)
    # Step 1: Get focused app
    selected_device = get_selected_device()
    serial_no = get_serial_number(selected_device)
    board, display_name = get_product_details(selected_device)
    focused_app = get_focused_app(selected_device)
    print(f"Detected focused app: {focused_app}")

    # Step 2: Select test suite based on focused app
    if "teams" in focused_app:
        test_target = "tests_scripts/tests_mtr"
        mode = "MTR"
    elif "zoom" in focused_app:
        test_target = "tests_scripts/tests_zoom"
        mode = "Zoom"
    elif "frogger" in focused_app:
        test_target = "tests_scripts/tests_device_mode"
        mode = "Device Mode"
    else:
        print("No specific test suite for the focused app. Running all tests.")
        test_target = "tests_scripts"

    # Step 3: Ensure reports directory exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Step 4: Generate report file with timestamp
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    report_file = f"reports/report_{test_target}_{timestamp}.html"

    # Step 5: Run pytest
    pytest.main([
        test_target,
        "-s",
        f"--html={report_file}",
        "--self-contained-html",
        "--metadata", "Serial NO", serial_no,
        "--metadata", "Board Details", board,
        "--metadata", "Display Name", display_name
    ])

    print(f"Test report generated: {report_file}")


if __name__ == "__main__":
    run_tests()
    print("All tests completed successfully.")