# Part 1 SQL outputs

Run `python data/generate_dataset.py` first, then `python part1_sql/queries.py`.

`monthly_category_revenue.csv` is the hand-off feed for Part 2 and Part 4. The other files answer the standing business questions:

- `region_revenue.csv`: revenue and order count by region.
- `top_resellers.csv`: the five resellers above INR 50,000 total spend.
- `zero_order_resellers.csv`: resellers with no matching order row.
- `zero_order_count_demo.csv`: the required LEFT JOIN counting demonstration.
- `june_delivered_aov.csv`: June delivered-order AOV.

For the zero-order reseller RS024, `COUNT(*) = 1` because a LEFT JOIN emits one all-NULL unmatched row, while `COUNT(order_id) = 0` because `order_id` is NULL on that row. Therefore `COUNT(*)` is the wrong test for a zero-match LEFT JOIN; use `COUNT(order_id) = 0` or `WHERE o.order_id IS NULL`.
