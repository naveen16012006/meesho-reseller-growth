"""Pure, testable guardrails and month-on-month growth functions."""
from __future__ import annotations

import csv
from typing import Tuple


def mom_growth(previous: float, current: float) -> float:
    if previous == 0:
        raise ValueError("previous revenue must be non-zero")
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    if abs(mom_pct) > threshold:
        return "flagged"
    if abs(mom_pct) < threshold:
        return "not_flagged"
    return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> Tuple[bool, list[str]]:
    errors: list[str] = []
    with open(csv_path, newline="") as handle:
        reader = csv.DictReader(handle)
        for line_number, row in enumerate(reader, start=2):
            category = (row.get("category") or "").strip()
            month = (row.get("month") or "").strip()
            revenue = (row.get("revenue") or "").strip()
            if not category:
                errors.append(f"line {line_number}: missing category (month={month})")
            if not revenue:
                errors.append(f"line {line_number}: missing revenue (category={category})")
            else:
                try:
                    parsed = float(revenue)
                except ValueError:
                    errors.append(f"line {line_number}: revenue not numeric: {revenue!r}")
                else:
                    if parsed < 0:
                        errors.append(f"line {line_number}: negative revenue ({parsed}) for category={category}")
    return (not errors, errors)
