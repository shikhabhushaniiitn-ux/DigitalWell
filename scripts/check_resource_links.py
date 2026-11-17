"""Manually check resource URLs and write a separate CSV status report.

This script is intentionally not imported by the Streamlit application. Run it
only when you want to make network requests to the official source URLs.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "resources" / "resources.csv"
DEFAULT_OUTPUT = ROOT / "reports" / "resource_link_check.csv"
TIMEOUT_SECONDS = 15


def check_url(url: str) -> tuple[str, str, str, str]:
    """Return status label, HTTP status, final URL, and error text."""
    try:
        parsed = urlparse(url)
    except ValueError:
        return "failed", "", "", "Malformed URL"
    if not url or parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "failed", "", "", "Missing or invalid HTTP(S) URL"
    request = Request(url, headers={"User-Agent": "DigitalWellLinkChecker/1.0"}, method="HEAD")
    try:
        response = urlopen(request, timeout=TIMEOUT_SECONDS)
    except HTTPError as exc:
        if exc.code in {405, 501}:
            try:
                response = urlopen(Request(url, headers={"User-Agent": "DigitalWellLinkChecker/1.0", "Range": "bytes=0-0"}, method="GET"), timeout=TIMEOUT_SECONDS)
            except HTTPError as fallback_error:
                final_url = fallback_error.geturl() or url
                label = "redirected" if final_url != url and 300 <= fallback_error.code < 400 else "failed"
                return label, str(fallback_error.code), final_url, str(fallback_error.reason)
            except (URLError, TimeoutError, OSError, ValueError) as fallback_error:
                return "failed", "", "", str(fallback_error)
        else:
            final_url = exc.geturl() or url
            label = "redirected" if final_url != url and 300 <= exc.code < 400 else "failed"
            return label, str(exc.code), final_url, str(exc.reason)
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return "failed", "", "", str(exc)

    with response:
        status_code = response.status
        final_url = response.geturl() or url
    label = "redirected" if final_url != url else ("reachable" if 200 <= status_code < 300 else "failed")
    error = "" if label != "failed" else f"Unexpected HTTP status {status_code}"
    return label, str(status_code), final_url, error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Resource CSV to read (never modified).")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Separate CSV report destination.")
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error(f"Input CSV not found: {args.input}")

    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = []
    with args.input.open("r", encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            original_url = (row.get("official_url") or "").strip()
            label, status_code, final_url, error = check_url(original_url)
            records.append({
                "resource_id": (row.get("id") or "").strip(),
                "resource_name": (row.get("name") or "").strip(),
                "url": original_url,
                "result": label,
                "http_status": status_code,
                "final_url": final_url,
                "checked_at_utc": checked_at,
                "error": error,
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["resource_id", "resource_name", "url", "result", "http_status", "final_url", "checked_at_utc", "error"]
    with args.output.open("w", encoding="utf-8", newline="") as report:
        writer = csv.DictWriter(report, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    counts = {label: sum(item["result"] == label for item in records) for label in ("reachable", "redirected", "failed")}
    print(f"Checked {len(records)} resource URLs at {checked_at}.")
    print("Results: " + ", ".join(f"{label}={count}" for label, count in counts.items()))
    print(f"Report: {args.output}")
    print("A reachable URL only confirms an HTTP response; it does not establish accuracy, safety, or endorsement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
