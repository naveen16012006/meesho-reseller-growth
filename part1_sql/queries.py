"""Run the five standing reseller-operations queries and write CSV outputs."""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "meesho_reseller.db"
OUT = Path(__file__).resolve().parent / "output"

QUERIES = {
    "monthly_category_revenue.csv": (
        "SELECT month, category, ROUND(SUM(quantity * unit_price), 2) AS revenue, "
        "COUNT(*) AS n_orders FROM orders GROUP BY month, category "
        "ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END, category"
    ),
    "region_revenue.csv": (
        "SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue, COUNT(*) AS n_orders "
        "FROM orders o JOIN resellers r ON r.reseller_id = o.reseller_id "
        "GROUP BY r.region ORDER BY revenue DESC"
    ),
    "top_resellers.csv": (
        "SELECT r.reseller_id, r.reseller_name, r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend "
        "FROM orders o JOIN resellers r ON r.reseller_id = o.reseller_id "
        "GROUP BY r.reseller_id, r.reseller_name, r.region HAVING total_spend > 50000 "
        "ORDER BY total_spend DESC LIMIT 5"
    ),
    "zero_order_resellers.csv": (
        "SELECT r.reseller_id, r.reseller_name, r.region FROM resellers r "
        "LEFT JOIN orders o ON o.reseller_id = r.reseller_id "
        "WHERE o.order_id IS NULL ORDER BY r.reseller_id"
    ),
    "june_delivered_aov.csv": (
        "SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS aov, COUNT(*) AS n_orders "
        "FROM orders WHERE month = 'June' AND status = 'Delivered'"
    ),
}

COUNT_STAR_EXPLANATION_QUERY = (
    "SELECT r.reseller_id, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id "
    "FROM resellers r LEFT JOIN orders o ON o.reseller_id = r.reseller_id "
    "WHERE r.reseller_id = 'RS024' GROUP BY r.reseller_id"
)


def write_query(conn: sqlite3.Connection, filename: str, sql: str) -> None:
    rows = conn.execute(sql).fetchall()
    headers = [column[0] for column in conn.execute(sql).description]
    with (OUT / filename).open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as conn:
        for filename, sql in QUERIES.items():
            write_query(conn, filename, sql)
        with (OUT / "zero_order_count_demo.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["reseller_id", "count_star", "count_order_id"])
            writer.writerows(conn.execute(COUNT_STAR_EXPLANATION_QUERY).fetchall())
    print(f"Wrote {len(QUERIES) + 1} query outputs to {OUT}")


if __name__ == "__main__":
    main()
