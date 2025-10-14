""" Test cases for TEAMS related testcases"""

import time
from datetime import datetime, timedelta, timezone
import json
import pytest
import os
from utils import get_auth_and_cookie
from modules import events as ev
from modules.extraction import dump_event_main, search_edid_file
from modules.version import get_collabos_version, get_collab_version_from_adb
from modules.mode import fetch_device_mode
import utils as util
from modules import generate_download as generate
util.have_auth()  # Ensure auth is available before running tests

def test_events_bort():
    """
    End-to-end check:
      1) build headers from config
      2) pick ADB device, reboot & wait
      3) poll the fixed window for Bort_DiskStats
    Passes when at least one Bort_DiskStats event is found.
    """
    # ---- 1) Headers / auth ----
    if not util.have_auth():
        pytest.skip("Missing auth in config/auth.txt or cookie in config/cookie.txt")
    try:
        headers = util.build_headers()
    except Exception as e:
        pytest.fail(f"Auth configuration error: {e}")
        return
    # ---- 2) Reboot device via ADB ----
    serial = None
    try:
        serial = util.get_selected_device()
    except Exception as e:
        pytest.skip(f"No online ADB device: {e}")
    reboot_ist = ev.reboot_and_wait(serial)
    # Build the fixed IST window used by the app code
    from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
    to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
    print(f"Fixed window (IST): {from_iso} to {to_iso}")
    # ---- 3) Poll for Bort_DiskStats ----
    deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
    found = False
    last_count = 0
    while datetime.now(ev.IST) < deadline and not found:
        page = ev.scan_window(headers, from_iso, to_iso)
        last_count = len(page)
        matches = [item for item in page if ev.is_bort_diskstats(item)]
        if matches:
            match = matches[0]
            ts = ev.ts_ms_to_ist(match.get("timestamp")) if "timestamp" in match else "n/a"
            print(f"Bort_DiskStats found at {ts}")
            found = True
            break
        print(f"…no match yet (scanned {last_count}). Sleeping {ev.POLL_INTERVAL_MIN} min")
        time.sleep(ev.POLL_INTERVAL_MIN * 60)
    assert found, f"Expected Bort_DiskStats not found (scanned last page count={last_count})"
    # ---- 4) Download the periodic bug report ----
    jwt, cookie = util.get_auth_and_cookie()
    from_time = generate.iso_z(datetime.fromisoformat(from_iso).astimezone(timezone.utc))
    to_time = generate.iso_z(datetime.fromisoformat(to_iso).astimezone(timezone.utc))
    downloaded_path = generate.poll_and_download_periodic(jwt, cookie, from_time, to_time, poll_every_sec=60)
    assert downloaded_path, "Failed to download periodic bug report"
    print(f"Downloaded periodic bug report to {downloaded_path}")
    # ---- 5) Extract events from the downloaded bug report ----
    try:
        search_found = dump_event_main()
        if not search_found:
            pytest.fail("Event extraction did not find expected events.")
    except Exception as e:
        pytest.fail(f"Event extraction failed: {e}")
        return


def test_events_display():
    """
    End-to-end check:
      1) build headers from config
      2) pick ADB device, reboot & wait
      3) poll the fixed window for Bort_DiskStats
    Passes when at least one Bort_DiskStats event is found.
    """
    # ---- 1) Headers / auth ----
    if not util.have_auth():
        pytest.skip("Missing auth in config/auth.txt or cookie in config/cookie.txt")
    try:
        headers = util.build_headers()
    except Exception as e:
        pytest.fail(f"Auth configuration error: {e}")
        return
    # ---- 2) Reboot device via ADB ----
    serial = None
    try:
        serial = util.get_selected_device()
    except Exception as e:
        pytest.skip(f"No online ADB device: {e}")
    reboot_ist = ev.reboot_and_wait(serial)
    # Build the fixed IST window used by the app code
    from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
    to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
    print(f"Fixed window (IST): {from_iso} to {to_iso}")
    # ---- 3) Poll for Bort_DiskStats ----
    deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
    found = False
    last_count = 0
    while datetime.now(ev.IST) < deadline and not found:
        page = ev.scan_window(headers, from_iso, to_iso)
        last_count = len(page)
        matches = [item for item in page if ev.is_connected_display(item)]
        if matches:
            match = matches[0]
            ts = ev.ts_ms_to_ist(match.get("timestamp")) if "timestamp" in match else "n/a"
            print(f"ConnectedDisplay found at {ts}")
            found = True
            break
        print(f"…no match yet (scanned {last_count}). Sleeping {ev.POLL_INTERVAL_MIN} min")
        time.sleep(ev.POLL_INTERVAL_MIN * 60)
    assert found, f"Expected ConnectedDisplay not found (scanned last page count={last_count})"


def test_device_mode_is_appliance():
    """
    call get_device_mode() from mode.py and assert
    the device mode equals "Appliance".
    """
    mode = fetch_device_mode()
    if mode:
        print(f"Mode is: {mode}")
        assert mode == "Appliance", "FAIL: DUT is not in Appliance Mode"
        print("PASS: DUT is in Appliance Mode")
    else:
        pytest.fail("Could not find Mode value on the page.")


def test_version_verification():
    """Test to verify the software version displayed on the web page matches the device version."""
    web_version = get_collabos_version()
    device = util.get_selected_device()
    device_version = get_collab_version_from_adb(device)
    assert device_version is not None, "Failed to retrieve version from device."
    assert web_version is not None, "Failed to extract version from web page."
    print(f"Device Version: {device_version}")
    print(f"Web Version: {web_version}")
    assert device_version == web_version, "Version mismatch between device and web page."


def test_on_demand_bugreport_appears():
    """ Test to trigger an on-demand bug report and verify its appearance. """
    # --- auth from your jenkins ---
    jwt, cookie = util.get_auth_and_cookie()
    if not (jwt or cookie):
        pytest.skip("Missing auth/cookie in ./config (auth.txt or cookie.txt)")
    trigger_time = generate.trigger_on_demand(generate.DEVICE)
    try:
        download_path = generate.poll_and_download_ondemand(
            jwt, cookie, trigger_time,
            poll_minutes=10, poll_every_sec=60
        )
    except TimeoutError:
        pytest.fail("ON-DEMAND bugreport did not appear within the poll window.")
    else:
        assert download_path and isinstance(download_path, str)
        print(f"Downloaded: {download_path}")

def test_edid_file():
    # --- auth from your config files ---
    jwt, cookie = get_auth_and_cookie()
    # jwt = generate.load(generate.AUTH_PATH)
    # cookie = generate.load(generate.COOKIE_PATH)
    if not (jwt or cookie):
        pytest.skip("Missing auth/cookie in ./config (auth.txt or cookie.txt)")

    # --- trigger via ADB (no download) ---
    trigger_time = generate.trigger_on_demand(generate.DEVICE)

    try:
        download_path = generate.poll_and_download_ondemand(
            jwt, cookie, trigger_time,
            poll_minutes=10, poll_every_sec=60
        )
    except TimeoutError:
        pytest.fail("✗ ON-DEMAND bugreport did not appear within the poll window.")
    else:
        assert download_path and isinstance(download_path, str)
        print(f"✓ Downloaded: {download_path}")
    # ---- 5) Extract events from the downloaded bug report ----
    try:
        search_edid_file()

    except Exception as e:
        pytest.fail(f"Event extraction failed: {e}")
        return


def test_search_all_events_with_wait():
    """
    Poll the event logs until each event listed in event_names.json appears
    (or until POLL_TIMEOUT_MIN expires).
    """
    # ---- load event names from JSON ----
    events_json = os.path.abspath("event_file.json")
    # here = os.path.dirname(__file__)
    # project_root = os.path.dirname(os.path.dirname(here))
    # events_json = os.path.join(project_root, "event_names.json")

    try:
        with open(events_json, "r", encoding="utf-8") as f:
            event_names = json.load(f)
        if not isinstance(event_names, list) or not all(isinstance(x, str) for x in event_names):
            raise ValueError("event_names.json must contain an array of strings.")
    except FileNotFoundError:
        pytest.skip("Missing event_names.json next to tests_mtr.py")
    except Exception as e:
        pytest.fail(f"Failed to read event_names.json: {e}")
        return


    if not util.have_auth():
        pytest.skip("Missing auth in config/auth.txt or cookie in config/cookie.txt")
    headers = util.build_headers()
    serial = util.get_selected_device()
    reboot_ist = ev.reboot_and_wait(serial)

    # ---- 2) Define time window ----
    from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
    to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
    print(f"\nPolling logs between {from_iso} and {to_iso}")

    # ---- 3) Poll until events appear ----
    deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
    found_events, missing_events = [], list(event_names)

    while datetime.now(ev.IST) < deadline and missing_events:
        page = ev.scan_window(headers, from_iso, to_iso)
        print(f"Scanned {len(page)} events at {datetime.now(ev.IST).strftime('%H:%M:%S')}")

        for name in list(missing_events):
            matches = [
                item for item in page
                if any(isinstance(v, str) and name.lower() in v.lower() for v in item.values())
            ]
            if matches:
                ts = matches[0].get("timestamp")
                when = ev.ts_ms_to_ist(ts) if ts else "unknown time"
                print(f"{name} found at {when}")
                found_events.append(name)
                missing_events.remove(name)

        if missing_events:
            print(f"Waiting for: {missing_events}")
            time.sleep(ev.POLL_INTERVAL_MIN * 60)
    print("\n===== Summary =====")
    print(f"Found: {found_events}")
    print(f"Missing: {missing_events}")
    assert not missing_events, f"Missing events after polling: {missing_events}"
def test_search_all_events_with_wait():
    """
    Poll the event logs until each event listed in event_file.json appears
    (or until POLL_TIMEOUT_MIN expires). For each found event, check whether
    the 'details' column is present and non-empty; print a warning if empty.
    """
    events_json = os.path.abspath("event_file.json")
    try:
        with open(events_json, "r", encoding="utf-8") as f:
            event_names = json.load(f)
        if not isinstance(event_names, list) or not all(isinstance(x, str) for x in event_names):
            raise ValueError("event_file.json must contain an array of strings.")
    except FileNotFoundError:
        pytest.skip("Missing event_file.json next to tests_mtr.py")
    except Exception as e:
        pytest.fail(f"Failed to read event_file.json: {e}")
        return

    if not util.have_auth():
        pytest.skip("Missing auth in config/auth.txt or cookie in config/cookie.txt")
    headers = util.build_headers()
    serial = util.get_selected_device()
    reboot_ist = ev.reboot_and_wait(serial)
    from_iso = ev.iso_ist(reboot_ist - timedelta(minutes=ev.PRE_REBOOT_MIN))
    to_iso = ev.iso_ist(reboot_ist + timedelta(minutes=ev.POST_REBOOT_MIN))
    print(f"\nPolling logs between {from_iso} and {to_iso}")
    deadline = datetime.now(ev.IST) + timedelta(minutes=ev.POLL_TIMEOUT_MIN)
    found_events, events = [], list(event_names)
    details_empty_events = []
    last_page = []
    while datetime.now(ev.IST) < deadline and events:
        page = ev.scan_window(headers, from_iso, to_iso)
        last_page = page
        print(f"Scanned {len(page)} events at {datetime.now(ev.IST).strftime('%H:%M:%S')}")
        for name in list(events):
            matches = [
                item for item in page
                if any(isinstance(v, str) and name.lower() in v.lower() for v in item.values())
            ]
            if matches:
                ts = matches[0].get("timestamp")
                when = ev.ts_ms_to_ist(ts) if ts else "unknown time"
                print(f"{name} found at {when}")
                details_value = None
                if "details" in matches[0]:
                    details_value = matches[0].get("details")
                    print(f"detail={details_value}")
                elif "DETAILS" in matches[0]:
                    details_value = matches[0].get("DETAILS")
                else:
                   for k, v in matches[0].items():
                        if isinstance(k, str) and k.lower() == "details":
                            details_value = v
                            break
                if details_value is None:
                    print(f"Details field MISSING for event: {name}")
                    details_empty_events.append(f"{name} (missing)")
                else:
                    try:
                        detail_str = details_value.strip() if isinstance(details_value, str) else str(
                            details_value).strip()
                    except Exception:
                        detail_str = str(details_value).strip()
                    if detail_str == "":
                        print(f"Details field EMPTY for event: {name}")
                        details_empty_events.append(f"{name} (empty)")
                found_events.append(name)
                events.remove(name)

        if events:
            print(f"Waiting for: {events}")
            time.sleep(ev.POLL_INTERVAL_MIN * 60)
    print(f"Found: {found_events}")
    print(f"Missing: {events}")
    if details_empty_events:
        print(f"Events with missing/empty details: {details_empty_events}")
        for entry in details_empty_events:
            evt_name = entry.split()[0]
            print(f"\n--- Last page entries similar to '{evt_name}' ---")
            for item in last_page:
                if evt_name.lower() in str(item).lower():
                    print(item)
    else:
        print("All found events have non-empty details.")
    assert not events, f"Missing events after polling: {events}"
