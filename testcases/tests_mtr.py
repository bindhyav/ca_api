""" Test cases for TEAMS related testcases"""

import time
from datetime import datetime, timedelta, timezone
import json
import pytest
import os
# from utils import get_auth_and_cookie
from modules import events as ev
# from modules.extraction import dump_event_main, extract_edid_file
# from modules.version import get_collabos_version, get_collab_version_from_adb
# from modules.mode import fetch_device_mode
import utils as util
# from modules import generate_download as generate
util.have_auth()

# def test_events_bort():
#     """
#     End-to-end check:
#       1) build headers from config
#       2) pick ADB device, reboot & wait
#       3) poll the fixed window for Bort_DiskStats
#     Passes when at least one Bort_DiskStats event is found.
#     """
#     # ---- 1) Headers / auth ----
#     if not util.have_auth():
#         pytest.skip("Missing auth in config/auth.txt or cookie in config/cookie.txt")
#     try:
#         headers = util.build_headers()
#     except Exception as e:
#         pytest.fail(f"Auth configuration error: {e}")
#         return
#     # ---- 2) Reboot device via ADB ----
#     serial = None
#     try:
#         serial = util.get_selected_device()
#     except Exception as e:
#         pytest.skip(f"No online ADB device: {e}")
#     reboot_ist = ev.reboot_and_wait(serial)
#     # Build the fixed IST window used by the app code
#     from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
#     to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
#     print(f"Fixed window (IST): {from_iso} to {to_iso}")
#     # ---- 3) Poll for Bort_DiskStats ----
#     deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
#     found = False
#     last_count = 0
#     while datetime.now(ev.IST) < deadline and not found:
#         page = ev.scan_window(headers, from_iso, to_iso)
#         last_count = len(page)
#         matches = [item for item in page if ev.is_bort_diskstats(item)]
#         if matches:
#             match = matches[0]
#             ts = ev.ts_ms_to_ist(match.get("timestamp")) if "timestamp" in match else "n/a"
#             print(f"Bort_DiskStats found at {ts}")
#             found = True
#             break
#         print(f"…no match yet (scanned {last_count}). Sleeping {ev.POLL_INTERVAL_MIN} min")
#         time.sleep(ev.POLL_INTERVAL_MIN * 60)
#     assert found, f"Expected Bort_DiskStats not found (scanned last page count={last_count})"
#     # ---- 4) Download the periodic bug report ----
#     jwt, cookie = util.get_auth_and_cookie()
#     from_time = generate.iso_z(datetime.fromisoformat(from_iso).astimezone(timezone.utc))
#     to_time = generate.iso_z(datetime.fromisoformat(to_iso).astimezone(timezone.utc))
#     downloaded_path = generate.poll_and_download_periodic(jwt, cookie, from_time, to_time, poll_every_sec=60)
#     assert downloaded_path, "Failed to download periodic bug report"
#     print(f"Downloaded periodic bug report to {downloaded_path}")
#     # ---- 5) Extract events from the downloaded bug report ----
#     try:
#         search_found = dump_event_main()
#         if not search_found:
#             pytest.fail("Event extraction did not find expected events.")
#     except Exception as e:
#         pytest.fail(f"Event extraction failed: {e}")
#         return
#
#
# def test_events_display():
#     """
#     End-to-end check:
#       1) build headers from config
#       2) pick ADB device, reboot & wait
#       3) poll the fixed window for Bort_DiskStats
#     Passes when at least one Bort_DiskStats event is found.
#     """
#     # ---- 1) Headers / auth ----
#     if not util.have_auth():
#         pytest.skip("Missing auth in config/auth.txt or cookie in config/cookie.txt")
#     try:
#         headers = util.build_headers()
#     except Exception as e:
#         pytest.fail(f"Auth configuration error: {e}")
#         return
#     # ---- 2) Reboot device via ADB ----
#     serial = None
#     try:
#         serial = util.get_selected_device()
#     except Exception as e:
#         pytest.skip(f"No online ADB device: {e}")
#     reboot_ist = ev.reboot_and_wait(serial)
#     # Build the fixed IST window used by the app code
#     from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
#     to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
#     print(f"Fixed window (IST): {from_iso} to {to_iso}")
#     # ---- 3) Poll for Bort_DiskStats ----
#     deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
#     found = False
#     last_count = 0
#     while datetime.now(ev.IST) < deadline and not found:
#         page = ev.scan_window(headers, from_iso, to_iso)
#         last_count = len(page)
#         matches = [item for item in page if ev.is_connected_display(item)]
#         if matches:
#             match = matches[0]
#             ts = ev.ts_ms_to_ist(match.get("timestamp")) if "timestamp" in match else "n/a"
#             print(f"ConnectedDisplay found at {ts}")
#             found = True
#             break
#         print(f"…no match yet (scanned {last_count}). Sleeping {ev.POLL_INTERVAL_MIN} min")
#         time.sleep(ev.POLL_INTERVAL_MIN * 60)
#     assert found, f"Expected ConnectedDisplay not found (scanned last page count={last_count})"


# def test_device_mode_is_appliance():
#     """
#     call get_device_mode() from mode.py and assert
#     the device mode equals "Appliance".
#     """
#     mode = fetch_device_mode()
#     if mode:
#         print(f"Mode is: {mode}")
#         assert mode == "Appliance", "FAIL: DUT is not in Appliance Mode"
#         print("PASS: DUT is in Appliance Mode")
#     else:
#         pytest.fail("Could not find Mode value on the page.")
#
#
# def test_version_verification():
#     """Test to verify the software version displayed on the web page matches the device version."""
#     web_version = get_collabos_version()
#     device = util.get_selected_device()
#     device_version = get_collab_version_from_adb(device)
#     assert device_version is not None, "Failed to retrieve version from device."
#     assert web_version is not None, "Failed to extract version from web page."
#     print(f"Device Version: {device_version}")
#     print(f"Web Version: {web_version}")
#     assert device_version == web_version, "Version mismatch between device and web page."
#
#
# def test_on_demand_bugreport_appears():
#     """ Test to trigger an on-demand bug report and verify its appearance. """
#     # --- auth from your jenkins ---
#     jwt, cookie = util.get_auth_and_cookie()
#     if not (jwt or cookie):
#         pytest.skip("Missing auth/cookie in ./config (auth.txt or cookie.txt)")
#     trigger_time = generate.trigger_on_demand(generate.DEVICE)
#     try:
#         download_path = generate.poll_and_download_ondemand(
#             jwt, cookie, trigger_time,
#             poll_minutes=10, poll_every_sec=60
#         )
#     except TimeoutError:
#         pytest.fail("ON-DEMAND bugreport did not appear within the poll window.")
#     else:
#         assert download_path and isinstance(download_path, str)
#         print(f"Downloaded: {download_path}")

# def test_edid_file():
#     # --- auth from your config files ---
#     jwt, cookie = get_auth_and_cookie()
#     # jwt = generate.load(generate.AUTH_PATH)
#     # cookie = generate.load(generate.COOKIE_PATH)
#     if not (jwt or cookie):
#         pytest.skip("Missing auth/cookie in ./config (auth.txt or cookie.txt)")
#
#     # --- trigger via ADB (no download) ---
#     trigger_time = generate.trigger_on_demand(generate.DEVICE)
#
#     try:
#         download_path = generate.poll_and_download_ondemand(
#             jwt, cookie, trigger_time,
#             poll_minutes=10, poll_every_sec=60
#         )
#     except TimeoutError:
#         pytest.fail("✗ ON-DEMAND bugreport did not appear within the poll window.")
#     else:
#         assert download_path and isinstance(download_path, str)
#         print(f"✓ Downloaded: {download_path}")
#     # ---- 5) Extract events from the downloaded bug report ----
#     try:
#         edid_file=extract_edid_file()
#         print(f"found edid file: {edid_file}")
#         assert edid_file,"edid file not found after extraction"
#     except Exception as e:
#         pytest.fail(f"Event extraction failed: {e}")
#         return

def test_events_from_json_simple():
    """
    Reads events from event_file.json and searches them in analytics logs.
    If key == "file", checks file extension from the list in JSON.
    """
    if not util.have_auth():
        pytest.skip("Missing auth/cookie")

    headers = util.build_headers()
    serial = util.get_selected_device()
    reboot_ist = ev.reboot_and_wait(serial)

    from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
    to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
    print(f"Scanning logs from {from_iso} to {to_iso}")

    here = os.path.dirname(__file__)
    project_root = os.path.dirname(here)
    events_json = os.path.join(project_root, "event_file.json")

    with open(events_json, "r", encoding="utf-8") as f:
        event_data = json.load(f)

    print(f"Loaded {len(event_data)} events from JSON")

    deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
    pending = event_data.copy()
    found = []

    while datetime.now(ev.IST) < deadline and pending:
        page = ev.scan_window(headers, from_iso, to_iso)
        print(f"Scanned {len(page)} events at {datetime.now(ev.IST).strftime('%H:%M:%S')}")

        for entry in list(pending):
            event_name = entry.get("event")
            key = entry.get("key")
            expected_value = entry.get("expected_value")  # may be list or string

            for item in page:
                if item.get("type") != event_name:
                    continue

                details = item.get("details", {})
                if isinstance(details, str):
                    try:
                        details = json.loads(details)
                    except Exception:
                        details = {}

                parameter = item.get(key)
                if not parameter:
                    parameter = details.get(key, "")

                if not isinstance(parameter, str):
                    parameters= str(parameter)

                # --- Case 1: key == "file" -> check extensions from JSON ---
                if key == "file":
                    # Ensure expected_value is a list
                    valid_extensions = expected_value if isinstance(expected_value, list) else [expected_value]
                    valid_extensions = [ext.lower().lstrip(".") for ext in valid_extensions]  # normalize
                    filename_lower = parameters.lower()
                    if any(filename_lower.endswith("." + ext) for ext in valid_extensions):
                        ts = item.get("timestamp")
                        when = ev.ts_ms_to_ist(ts) if ts else "unknown"
                        print(f"{event_name}: file '{parameters}' has valid extension at {when}")
                        found.append(event_name)
                        pending.remove(entry)
                    else:
                        print(f"{event_name}: file '{parameters}' does NOT have a valid extension {valid_extensions}")
                        continue

                # --- Case 2: handle non-file keys ---
                if isinstance(expected_value, str) and expected_value == "__not_empty__":
                    if parameters.strip():
                        ts = item.get("timestamp")
                        when = ev.ts_ms_to_ist(ts) if ts else "unknown"
                        print(f"{event_name}: '{key}' is non-empty ('{parameters}') at {when}")
                        found.append(event_name)
                        pending.remove(entry)

                    else:
                        print(f"{event_name}: '{key}' empty or missing (value={parameters!r})")
                        continue

                # Normal matching logic
                if isinstance(expected_value, list):
                    matched = any(str(v).lower() in parameters.lower() for v in expected_value)
                else:
                    matched = str(expected_value).lower() in parameters.lower()

                if matched:
                    ts = item.get("timestamp")
                    when = ev.ts_ms_to_ist(ts) if ts else "unknown"
                    print(f"{event_name}: '{key}' contains expected '{expected_value}' at {when}")
                    found.append(event_name)
                    pending.remove(entry)

                else:
                    print(f"{event_name}: candidate '{parameters}' does not match '{expected_value}'")

        if pending:
            print(f"Waiting for: {[p['event'] for p in pending]}")
            time.sleep(ev.POLL_INTERVAL_MIN * 60)

    print("\n===== Summary =====")
    print(f"Found: {found}")
    print(f"Missing: {[p['event'] for p in pending]}")
    assert not pending, f"Missing or unmatched events: {[p['event'] for p in pending]}"