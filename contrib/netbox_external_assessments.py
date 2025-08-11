#!/usr/bin/env python3
"""
NetBox LCM External Assessments REST helper

Supports:
  - add/update ExternalAssessmentType
  - publish ExternalAssessment for a Device

Usage examples:

  # Add/Update a type
  python netbox_external_assessments.py --url https://netbox.example/api --token $NETBOX_TOKEN \
    add-type --slug nac --label "NAC Compliance" --retention 90 --higher-is-better true --ui-badge success

  # Publish an assessment for a device by NAME
  python netbox_external_assessments.py --url https://netbox.example/api --token $NETBOX_TOKEN \
    publish-device --device-name sw-core-01 --type nac --source nac-pipeline \
    --status FAIL --score 72.5 --summary "3 non-compliant ports" \
    --details '{"non_compliant_ports":["Gi1/0/10","Gi1/0/12","Gi1/0/47"]}' \
    --external-url https://reports.example/run/abc123

  # Publish an assessment for a device by ID
  python netbox_external_assessments.py --url https://netbox.example/api --token $NETBOX_TOKEN \
    publish-device --device-id 1234 --type nac --source nac-pipeline --status PASS --score 100
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone as pytimezone

import requests

# -------- Helpers --------

def _headers(token: str) -> dict:
    return {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

def _api_url(base_api_url: str, path: str) -> str:
    base = base_api_url.rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}"

def _iso_now() -> str:
    return datetime.now(tz=pytimezone.utc).isoformat()

def _get_device_id_by_name(base_api_url: str, token: str, name: str, verify=True) -> int:
    url = _api_url(base_api_url, f"dcim/devices/?name={name}")
    r = requests.get(url, headers=_headers(token), verify=verify, timeout=30)
    r.raise_for_status()
    data = r.json()
    count = data.get("count", 0)
    if count == 0:
        raise SystemExit(f"Device named '{name}' not found")
    if count > 1:
        # Prefer exact name match on the first result—NetBox should return exact, but warn if multiple
        raise SystemExit(f"Multiple devices named '{name}' found (count={count}); use --device-id instead.")
    return data["results"][0]["id"]

# -------- Actions --------

def add_or_update_type(base_api_url: str, token: str, *, slug: str, label: str | None,
                       retention: int, higher_is_better: bool, ui_badge: str, verify=True):
    """
    POST if new; PATCH if exists.
    """
    list_url = _api_url(base_api_url, "plugins/lifecycle/external-assessment-types/")
    # Try GET detail via list filter (plugin viewset in scaffold is read-only)
    r = requests.get(f"{list_url}?slug={slug}", headers=_headers(token), verify=verify, timeout=30)
    r.raise_for_status()
    existing = r.json()
    payload = {
        "slug": slug,
        "label": label or slug,
        "default_retention_days": retention,
        "higher_is_better": higher_is_better,
        "ui_badge": ui_badge or "default",
    }

    if isinstance(existing, dict) and existing.get("count", 0) == 1:
        # Update via PATCH requires the object URL; fetch the ID and call detail endpoint
        obj = existing["results"][0]
        detail_url = _api_url(base_api_url, f"plugins/lifecycle/external-assessment-types/{obj['slug']}/")
        r = requests.patch(detail_url, headers=_headers(token), data=json.dumps(payload), verify=verify, timeout=30)
        r.raise_for_status()
        print(f"Updated type '{slug}'")
    else:
        # Create (Note: the scaffold’s ViewSet is ReadOnly; if you keep it RO, create via Django admin/scripts)
        # If you DO expose create server-side, this will work:
        r = requests.post(list_url, headers=_headers(token), data=json.dumps(payload), verify=verify, timeout=30)
        if r.status_code in (200, 201):
            print(f"Created type '{slug}'")
        else:
            # If the endpoint is read-only you'll get 405 here.
            print(f"Create attempt returned {r.status_code}: {r.text}")
            r.raise_for_status()

def publish_device_assessment(base_api_url: str, token: str, *,
                              device_id: int | None, device_name: str | None,
                              assessment_type: str, source: str, status: str,
                              score: float | None, summary: str | None,
                              details: dict | None, external_url: str | None,
                              observed_at: str | None, expires_at: str | None,
                              retention_days: int | None, source_run_id: str | None,
                              external_reference: str | None, verify=True):
    """
    POST an ExternalAssessment for a device.
    """
    if not device_id and not device_name:
        raise SystemExit("Provide --device-id or --device-name")
    if device_name and not device_id:
        device_id = _get_device_id_by_name(base_api_url, token, device_name, verify=verify)

    payload = {
        "assessment_type": assessment_type,
        "target_type": "dcim.device",             # matches serializer in scaffold
        "target_id": device_id,
        "source": source,
        "source_run_id": source_run_id or None,
        "external_reference": external_reference or None,
        "observed_at": observed_at or _iso_now(),
        "expires_at": expires_at or None,
        "retention_days": retention_days if retention_days is not None else 90,
        "status": status,                          # PASS/FAIL/EXEMPT/UNKNOWN
        "score": score,                            # may be None
        "summary": summary or "",
        "details": details or {},
        "external_url": external_url or None,
    }

    url = _api_url(base_api_url, "plugins/lifecycle/external-assessments/")
    r = requests.post(url, headers=_headers(token), data=json.dumps(payload), verify=verify, timeout=60)
    if r.status_code not in (200, 201):
        print(f"ERROR {r.status_code}: {r.text}")
        r.raise_for_status()
    obj = r.json()
    print(f"Created assessment id={obj.get('id')} type={obj['assessment_type']} device_id={obj['target_id']} "
          f"status={obj['status']} score={obj.get('score')} observed_at={obj['observed_at']}")
    return obj

# -------- CLI --------

def main():
    parser = argparse.ArgumentParser(description="NetBox External Assessments REST helper")
    parser.add_argument("--url", required=True, help="Base API URL, e.g. https://netbox.example/api")
    parser.add_argument("--token", default=os.getenv("NETBOX_TOKEN"), help="NetBox API Token (or NETBOX_TOKEN env var)")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # add-type
    p1 = sub.add_parser("add-type", help="Create or update an assessment type")
    p1.add_argument("--slug", required=True)
    p1.add_argument("--label")
    p1.add_argument("--retention", type=int, default=90)
    p1.add_argument("--higher-is-better", type=lambda s: s.lower() in ("1","true","yes"), default=True)
    p1.add_argument("--ui-badge", default="default")

    # publish-device
    p2 = sub.add_parser("publish-device", help="Publish an assessment for a device")
    tgt = p2.add_mutually_exclusive_group(required=True)
    tgt.add_argument("--device-id", type=int)
    tgt.add_argument("--device-name")
    p2.add_argument("--type", dest="assessment_type", required=True)
    p2.add_argument("--source", required=True)
    p2.add_argument("--status", required=True, choices=["pass","fail","exempt","unknown"])
    p2.add_argument("--score", type=float)
    p2.add_argument("--summary")
    p2.add_argument("--details", help="JSON string or @/path/to/file.json")
    p2.add_argument("--external-url")
    p2.add_argument("--observed-at", help="ISO8601, default now (UTC)")
    p2.add_argument("--expires-at", help="ISO8601")
    p2.add_argument("--retention-days", type=int, default=90)
    p2.add_argument("--source-run-id")
    p2.add_argument("--external-reference")

    args = parser.parse_args()
    if not args.token:
        raise SystemExit("Provide --token or set NETBOX_TOKEN env var")

    verify = not args.insecure

    if args.cmd == "add-type":
        add_or_update_type(
            args.url, args.token,
            slug=args.slug,
            label=args.label,
            retention=args.retention,
            higher_is_better=args.higher_is_better,
            ui_badge=args.ui_badge,
            verify=verify
        )
    elif args.cmd == "publish-device":
        # details parsing (string or @file)
        details = None
        if args.details:
            if args.details.startswith("@"):
                path = args.details[1:]
                with open(path, "r", encoding="utf-8") as fh:
                    details = json.load(fh)
            else:
                details = json.loads(args.details)

        publish_device_assessment(
            args.url, args.token,
            device_id=args.device_id,
            device_name=args.device_name,
            assessment_type=args.assessment_type,
            source=args.source,
            status=args.status,
            score=args.score,
            summary=args.summary,
            details=details,
            external_url=args.external_url,
            observed_at=args.observed_at,
            expires_at=args.expires_at,
            retention_days=args.retention_days,
            source_run_id=args.source_run_id,
            external_reference=args.external_reference,
            verify=verify
        )

if __name__ == "__main__":
    main()
