"""Offline mock agent: validate, compare, rank, draft, suppress, and hold."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "part2_engine"))
sys.path.insert(0, str(ROOT / "part3_narrative"))

from growth_engine import is_flagged, mom_growth, validate_feed
from prompt_pack import fill_flagged_template


def read_revenues(path: str) -> dict[str, float]:
    with open(path, newline="") as handle:
        return {row["category"]: float(row["revenue"]) for row in csv.DictReader(handle)}


def read_month(path: str) -> str:
    with open(path, newline="") as handle:
        return next(csv.DictReader(handle))["month"]


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    valid, errors = validate_feed(current_month_csv)
    result = {
        "run_month": month,
        "validation_status": "valid" if valid else "invalid",
        "validation_errors": errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": "drafted_and_held_for_approval" if valid else "hard_stop",
    }
    if not valid:
        return result

    previous = read_revenues(previous_month_csv)
    current = read_revenues(current_month_csv)
    previous_month = read_month(previous_month_csv)
    comparisons = []
    for category, current_revenue in current.items():
        if category not in previous:
            raise ValueError(f"category missing from previous feed: {category}")
        pct = mom_growth(previous[category], current_revenue)
        status = is_flagged(pct)
        comparisons.append((category, pct, previous[category], current_revenue, status))

    comparisons.sort(key=lambda item: abs(item[1]), reverse=True)
    flagged = [item for item in comparisons if item[4] == "flagged"]
    exact_boundary = [item[0] for item in comparisons if item[4] == "escalate_exact_boundary"]
    result["escalated_categories"] = exact_boundary
    for index, (category, pct, previous_revenue, current_revenue, _status) in enumerate(flagged):
        entry = {
            "category": category,
            "mom_pct": pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
            "drafted": index < 3,
        }
        if index < 3:
            entry["message"] = fill_flagged_template(
                category, previous_revenue, current_revenue, pct, month,
                previous_month,
            )
            result["flagged_categories"].append(entry)
        else:
            result["suppressed_categories"].append(category)
    return result


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("Usage: python part4_agent/mock_agent_runner.py MONTH PREVIOUS_CSV CURRENT_CSV")
    print(json.dumps(run(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2))


if __name__ == "__main__":
    main()
