# Stakeholder narrative report

## May Ethnic Wear: Context → Insight → Implication

**Context.** This measures Ethnic Wear revenue from April to May 2026: INR 104520.77 in April compared with INR 185107.61 in May.

**Insight (fact).** Ethnic Wear revenue increased **77.1% month on month** in May versus April, so the category is flagged by the 8% rule.

**Implication (hypothesis).** A regional manager should review the May Ethnic Wear assortment, pricing, and reseller availability, then prioritize replenishment or promotion for the strongest verified product and region signals; the cause of the increase is a hypothesis until those checks are completed.

**Self-score.** Specificity passes because the category, months, revenues, and 77.1% are exact. Audience fit passes because the wording gives a regional manager a practical operating decision. Completeness passes because Context, Insight, and Implication are all present. Actionability passes because the next step names assortment, pricing, availability, and prioritization rather than merely saying to investigate.

## June Ethnic Wear: Context → Insight → Implication

**Context.** This measures Ethnic Wear revenue from May to June 2026: INR 185107.61 in May compared with INR 76371.53 in June.

**Insight (fact).** Ethnic Wear revenue decreased **58.74% month on month** in June versus May, so the category is flagged in the opposite direction by the 8% rule.

**Implication (hypothesis).** A regional manager should first check June stock availability, assortment continuity, and reseller activation for Ethnic Wear, then restore the best-supported assortment or promotion only after confirming which operational factor changed; any causal explanation remains a hypothesis until verified.

**Self-score.** Specificity passes because the category, months, revenues, and -58.74% are exact. Audience fit passes because the recommendation is framed for a regional manager's operational review. Completeness passes because Context, Insight, and Implication are all present. Actionability passes because it names stock, assortment, reseller activation, and a concrete restore-or-hold decision.

## Chart-choice justification

**Which month had the highest total revenue?** Use a vertical bar chart with one bar per month and the y-axis starting at zero. This is a univariate comparison of one measure across a categorical month dimension; the bars make the highest month clear within 10 seconds without a legend or 3D decoration. The values are April INR 419417.43, May INR 444594.25, and June INR 398055.24, so May is highest.

**What percentage share does Ethnic Wear represent of April's total revenue?** Use a 100% stacked bar or a single proportion-focused donut only if the audience needs a quick composition view; I would choose a 100% stacked bar because it keeps the comparison anchored to a common whole and avoids a misleading non-zero axis. This is a bivariate part-to-whole question: Ethnic Wear is INR 104520.77 of April's INR 419417.43, or 24.92%. A single series needs no legend beyond direct labeling.

**How do the four regions compare on total revenue?** Use a sorted horizontal bar chart with a zero-starting x-axis. This is a univariate comparison across four regional categories, and sorting makes the ranking legible within 10 seconds without a legend because there is only one series. North is INR 337125.46, West INR 333106.33, South INR 316736.68, and East INR 275098.45; no 3D treatment is needed.

## Masking demonstration

The top-spend narrative uses only coded aliases and regions: **West ALIAS-19** (INR 75295.09), **West ALIAS-22** (INR 73882.33), **South ALIAS-12** (INR 69936.46), **North ALIAS-06** (INR 64238.97), and **North ALIAS-05** (INR 61825.02). The raw reseller names are intentionally omitted. `alias_for("RS019")` returns `ALIAS-19`; `assert_no_raw_names_leak` returns `True` for this safe text and `False` for a test string containing `Mumbai Reseller 1`.
