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
    Simplified test:
    - Reads event_file.json.
    - For each event, searches in logs for the given 'key' field (e.g., file or path).
    - Passes if the field value ends with any extension in expected_value (e.g., .zip, .tar, .mar).
    - Only checks what's in JSON; no extra conditions.
    """
    if not util.have_auth():
        pytest.skip("Missing auth/cookie")

    headers = util.build_headers()
    serial = util.get_selected_device()
    reboot_ist = ev.reboot_and_wait(serial)

    from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
    to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
    here = os.path.dirname(__file__)
    events_json = os.path.join(os.path.dirname(here), "event_file.json")

    with open(events_json, "r", encoding="utf-8") as f:
        event_data = json.load(f)

    pending = [dict(e) for e in event_data]
    found = []
    deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)

    while datetime.now(ev.IST) < deadline and pending:
        page = ev.scan_window(headers, from_iso, to_iso)
        print(f"Scanned {len(page)} events")

        for entry in list(pending):
            event_name = entry["event"]
            key = entry["key"]
            expected = entry["expected_value"]
            matched = False

            for raw_item in page:
                # Ensure dict format
                item = raw_item
                if isinstance(raw_item, str):
                    try:
                        item = json.loads(raw_item)
                    except Exception:
                        continue
                if not isinstance(item, dict):
                    continue

                # Match event type
                if item.get("type") != event_name:
                    continue

                # Get field value (top or inside details)
                value = ""
                if key in item and item[key]:
                    value = str(item[key])
                else:
                    details = item.get("details", {})
                    if isinstance(details, str):
                        try:
                            details = json.loads(details)
                        except Exception:
                            details = {}
                    if isinstance(details, dict) and key in details:
                        value = str(details[key])

                if not value:
                    continue  # skip if field not present

                # Extract filename and extension
                filename = os.path.basename(value.split("?",maxsplit=1)[0])
                _, ext = os.path.splitext(filename)
                ext = ext.lower().lstrip(".")

                # Normalize expected extensions
                valid_extension = expected if isinstance(expected, list) else [expected]
                valid_extension = [str(e).lower().lstrip(".") for e in valid_extension]

                # Match extension
                if ext in valid_extension:
                    print(f"[{event_name}] Found valid {key}: '{filename}' (.{ext})")
                    found.append(event_name)
                    pending.remove(entry)
                    matched = True

                else:
                    print(f"[{event_name}] {key}='{filename}' invalid ext '.{ext}', expected {valid_extension}")

            if matched:
                continue

        if pending:
            print(f"Waiting for: {[p['event'] for p in pending]}")
            time.sleep(ev.POLL_INTERVAL_MIN * 60)

    print("\n===== Summary =====")
    print(f"Found: {found}")
    print(f"Missing: {[p['event'] for p in pending]}")
    assert not pending, f"Missing or invalid events: {[p['event'] for p in pending]}"

