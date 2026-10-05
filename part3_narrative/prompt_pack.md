# Reusable prompt pack

## Trigger
Start this prompt when a category's `is_flagged` result is exactly `flagged`.

## Input list
The template requires `{category}`, `{previous_revenue}`, `{current_revenue}`, `{mom_pct}`, `{month}`, and `{prev_month}`. These values must come directly from the validated Part 1 feed and Part 2 calculations.

## Prompt
> Write a stakeholder update for a regional manager using the **Context → Insight → Implication** structure. Context must name the category and both months and state the supplied revenue values. Insight must state the supplied month-on-month percentage and label it as a fact. Implication must give one specific, actionable next step and label any proposed cause as a hypothesis. Use only the supplied placeholders `{category}`, `{previous_revenue}`, `{current_revenue}`, `{mom_pct}`, `{month}`, and `{prev_month}` for numeric or factual claims. Never invent, estimate, round differently, or add a number that is not present in the inputs. Never expose a raw reseller name; use a coded alias if a reseller is relevant.

## Checklist

1. Does every number in the draft match a supplied placeholder value, using the same displayed precision?
2. Are the Context, Insight, and Implication sections all present and clearly labeled?
3. Is the insight labeled as a fact and every unproven causal explanation labeled as a hypothesis?
4. Is the recommendation specific and actionable for a regional manager rather than a vague request to investigate?
5. Does the text avoid all raw reseller names and use only coded aliases where needed?
6. Does the category and both month names match the feed row and comparison period exactly?
