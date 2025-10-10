import subprocess
import re
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import time

log_file_path = "window_dump.xml"
LOGIN_URL = "https://microsoft.com/devicelogin"
LOGIN_EMAIL = "logi-eng-mtr33@logi-df.com"
LOGIN_PASSWORD = "Logi123!52160"

def run_adb_commands():
    try:
        subprocess.run(["adb", "shell", "uiautomator", "dump"], check=True)
        subprocess.run(["adb", "pull", "/sdcard/window_dump.xml"], check=True)
        print("[INFO] UI dump pulled successfully.")
    except Exception as e:
        print(f"[ERROR] ADB command failed: {e}")

def read_cmd_output_safe():
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            return f.read().lower()
    except Exception as e:
        print(f"[ERROR] Reading log failed: {e}")
        return ""

def extract_device_code_from_xml():
    try:
        tree = ET.parse(log_file_path)
        root = tree.getroot()
        for node in root.iter("node"):
            text = node.attrib.get("text", "")
            if re.fullmatch(r"[A-Z0-9]{9}", text):
                return text
    except Exception as e:
        print(f"[ERROR] Could not extract device code: {e}")
    return None

def login_with_device_code(device_code):
    print(f"[INFO] Login with device's code: {device_code}")
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(LOGIN_URL)
        wait.until(ec.visibility_of_element_located((By.ID, "otc"))).send_keys(device_code)
        wait.until(ec.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        wait.until(ec.visibility_of_element_located((By.ID, "i0116"))).send_keys(LOGIN_EMAIL)
        wait.until(ec.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        wait.until(ec.visibility_of_element_located((By.ID, "i0118"))).send_keys(LOGIN_PASSWORD)
        wait.until(ec.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        wait.until(ec.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        time.sleep(5)
        print("[SUCCESS] Microsoft Authentication Completed.")
    except Exception as e:
        print(f"[ERROR] Authentication failed: {e}")
    finally:
        driver.quit()

def main():
    run_adb_commands()
    code = extract_device_code_from_xml()
    if code:
        print(f"Device login code found: {code}")
    else:
        print("No valid device login code found.")
    login_with_device_code(code)

if __name__ == "__main__":
    main()