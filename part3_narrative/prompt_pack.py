"""Offline deterministic narrative template used by Part 4."""


def fill_flagged_template(category: str, previous_revenue: float, current_revenue: float,
                          mom_pct: float, month: str, prev_month: str) -> str:
    pct_text = format(mom_pct, "g")
    return (
        f"Context: {category} revenue moved from INR {previous_revenue:.2f} in {prev_month} "
        f"to INR {current_revenue:.2f} in {month}.\n"
        f"Insight (fact): Month-on-month revenue change was {pct_text}%.\n"
        f"Implication (hypothesis): The regional manager should review {category} assortment, "
        f"pricing, and reseller availability for {month}, then act on the highest-confidence finding."
    )
