# Meesho Reseller Growth & Alert Intelligence Pipeline

This repository implements the four-part offline reseller-operations monitoring pipeline from seeded data generation through guarded narrative drafting. It needs Python 3.9+ and the standard library only. **No API key, paid service, hosted account, or network connection is required.**

## Run the pipeline in order

From the repository root:

```bash
python data/generate_dataset.py
python part1_sql/queries.py
cp part1_sql/output/monthly_category_revenue.csv part2_engine/fixtures/monthly_category_revenue.csv
python part2_engine/test_growth_engine.py
```

The generator is fixed at seed 42 and writes 24 resellers, 900 orders, and `data/meesho_reseller.db`. Part 1 runs the five standing SQLite queries and writes CSVs under `part1_sql/output/`. Its `monthly_category_revenue.csv` is the direct feed into Parts 2 and 4. The copy command places that feed in the Part 2 fixture directory so the validation test is self-contained.

Run the Part 4 scenarios after the copy. Create month-specific CSVs from the Part 1 output or use the small driver below. The runner's API is `run(month, previous_month_csv, current_month_csv)` and returns the required JSON object. A convenient example using filtered feeds is:

```bash
python - <<'PY'
import csv
from pathlib import Path

source = Path('part2_engine/fixtures/monthly_category_revenue.csv')
rows = list(csv.DictReader(source.open()))
for month in ('April', 'May', 'June'):
    with Path(f'/tmp/{month.lower()}.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['month','category','revenue','n_orders'])
        writer.writeheader(); writer.writerows(r for r in rows if r['month'] == month)
PY
python part4_agent/mock_agent_runner.py May /tmp/april.csv /tmp/may.csv
python part4_agent/mock_agent_runner.py June /tmp/may.csv /tmp/june.csv
python part4_agent/mock_agent_runner.py July /tmp/may.csv part2_engine/fixtures/corrupted_feed.csv
```

The invalid-feed command must return `validation_status: "invalid"`, `action_taken: "hard_stop"`, the three ordered errors, and empty flagged/suppressed lists. May drafts the top three flagged categories by absolute magnitude and suppresses the remaining two; June drafts three, suppresses Western Wear, and excludes Beauty & Personal Care because it is below threshold.

## Part map

**Part 1 → Part 2** follows the safe order of computing real numbers in SQL first and handing the verified feed to a numeric guardrail engine. **Part 2 → Part 3** turns a tested change classification into a constrained prompt pack and deterministic template-fill narrative. **Part 4** mirrors an Intake → Summary → Report Draft → Validate reporting flow: intake validation is a hard gate, the summary is computed from the feed, drafts are capped and held for approval, and the JSON output makes suppression and exact-boundary escalation explicit.

## Repository contents

- `data/`: the verbatim seeded generator and generated CSV/SQLite data.
- `part1_sql/`: query runner and output CSVs, including the `COUNT(*)` versus `COUNT(order_id)` demonstration.
- `part2_engine/`: `mom_growth`, `is_flagged`, `validate_feed`, fixtures, and Given-When-Then tests.
- `part3_narrative/`: prompt pack, worked narrative report, deterministic template fill, and reseller masking.
- `part4_agent/`: agent specification and mock runner with validation hard stop, top-three cap, suppression, escalation, and human-held drafts.

The narrative path is deterministic and offline by design. Optional real-LLM integration is deliberately out of scope so the full acceptance path remains reproducible with zero credentials.

## Documentation note

Implementation uses Python standard-library modules (`random`, `sqlite3`, `csv`, `os`, `pathlib`, and `json`). The relevant official reference is the [Python 3 Standard Library documentation](https://docs.python.org/3/library/).
