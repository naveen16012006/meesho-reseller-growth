# Part 4: monitoring agent specification

## Goal
Keep Meesho category managers informed of any category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every drafted message before it goes out.

## Tools
The agent calls `validate_feed`, `mom_growth`, and `is_flagged` from Part 2 without re-implementing them. It calls Part 3's deterministic `fill_flagged_template` to draft stakeholder text and uses the masking helpers for any reseller reference.

## Memory / state
Each run receives the previous month's category-revenue feed and the current month's feed. The previous revenue per category is the state needed to compute the next MoM comparison; the runner does not retain hidden state between invocations.

## Planner and ordered subtasks

1. Load the monthly revenue feed and run `validate_feed`.
2. If validation fails, Hard Stop and report the errors.
3. If valid, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by absolute MoM percentage descending.
6. Draft a message through Part 3's template for at most the top three flagged categories.
7. Log any remaining flagged categories as `suppressed, review manually` without drafting them.
8. Separately log exact-boundary categories in `escalated_categories` without drafting them.
9. Emit one structured JSON object for the run.

## Feedback loop
Every draft is held for human approval. The runner simulates this checkpoint using `action_taken = drafted_and_held_for_approval`; it never sends email, calls a network service, or marks a draft as approved.

## Guardrails

- **Input:** `validate_feed` must pass before any MoM computation or drafting runs.
- **Action:** no message is auto-sent; messages are drafted and held only.
- **Output:** every number in a draft traces to a Part 1 feed value or a Part 2 calculation; no invented figures are permitted.

## Success and error stopping conditions
Success means drafts were produced, or correctly zero drafts were produced, with every number traceable. An invalid feed is an error: `validate_feed` returns `False`, the run is a Hard Stop, and all validation errors are surfaced rather than silently skipped.

## Given-When-Then agent specs

- **Given** April Ethnic Wear revenue is INR 104520.77 and May revenue is INR 185107.61, **when** the agent computes and classifies the change, **then** MoM is 77.1% and the category is `flagged`.
- **Given** May Beauty & Personal Care revenue is INR 35542.11 and June revenue is INR 37559.07, **when** the agent evaluates it, **then** MoM is 5.67% and the category is `not_flagged`.
- **Given** previous revenue is INR 100000 and current revenue is INR 108000, **when** the agent evaluates the exact boundary, **then** MoM is exactly 8.0% and the result is `escalate_exact_boundary`.
- **Given** the corrupted feed, **when** the agent validates it, **then** it Hard Stops with exactly the three ordered validation errors and performs no MoM computation.
