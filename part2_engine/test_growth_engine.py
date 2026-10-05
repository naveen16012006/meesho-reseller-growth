import csv
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from growth_engine import is_flagged, mom_growth, validate_feed

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "part2_engine" / "fixtures"


def revenues(path):
    with path.open(newline="") as handle:
        return {(row["month"], row["category"]): float(row["revenue"]) for row in csv.DictReader(handle)}


def test_may_ethnic_flagged():
    assert mom_growth(104520.77, 185107.61) == 77.1
    assert is_flagged(77.1) == "flagged"


def test_june_beauty_not_flagged():
    assert mom_growth(35542.11, 37559.07) == 5.67
    assert is_flagged(5.67) == "not_flagged"


def test_exact_boundary_escalates():
    assert mom_growth(100000, 108000) == 8.0
    assert is_flagged(8.0) == "escalate_exact_boundary"


def test_corrupted_feed_errors_in_order():
    valid, errors = validate_feed(str(FIXTURES / "corrupted_feed.csv"))
    assert valid is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]


def test_valid_feed_passes():
    valid, errors = validate_feed(str(FIXTURES / "monthly_category_revenue.csv"))
    assert (valid, errors) == (True, [])


def test_full_may_table():
    values = revenues(FIXTURES / "monthly_category_revenue.csv")
    expected = {
        "Ethnic Wear": (104520.77, 185107.61, 77.1),
        "Western Wear": (113866.15, 86998.18, -23.6),
        "Kids Wear": (59847.27, 45793.78, -23.48),
        "Home & Kitchen": (100446.23, 91152.57, -9.25),
        "Beauty & Personal Care": (40737.01, 35542.11, -12.75),
    }
    for category, (previous, current, expected_growth) in expected.items():
        assert mom_growth(values[("April", category)], values[("May", category)]) == expected_growth
        assert is_flagged(expected_growth) == "flagged"


def test_full_june_table():
    values = revenues(FIXTURES / "monthly_category_revenue.csv")
    expected = {
        "Ethnic Wear": (-58.74, "flagged"),
        "Western Wear": (11.97, "flagged"),
        "Kids Wear": (23.9, "flagged"),
        "Home & Kitchen": (42.59, "flagged"),
        "Beauty & Personal Care": (5.67, "not_flagged"),
    }
    for category, (expected_growth, status) in expected.items():
        assert mom_growth(values[("May", category)], values[("June", category)]) == expected_growth
        assert is_flagged(expected_growth) == status


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f" passed: {len(tests)} tests")
