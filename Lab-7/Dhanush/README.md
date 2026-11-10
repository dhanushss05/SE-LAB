# Lab 7: Fuzz Testing — Parking Fee

**Name:** Dhanush S S | **SRN:** PES1UG24AM082 | **Section:** B
**Assigned repo:** [SETAPESU26/L6_L7_19_parking_fee](https://github.com/SETAPESU26/L6_L7_19_parking_fee) (Lab 7 folder)

## Deliverables

| # | Deliverable | File |
|---|-------------|------|
| 1 | PDF document with screenshots | [`Lab7_PES1UG24AM082_FuzzTesting.pdf`](Lab7_PES1UG24AM082_FuzzTesting.pdf) |
| 2 | Fixed application script | [`parking_fee.py`](parking_fee.py) |
| 3 | Updated test file | [`test_parking_fee.py`](test_parking_fee.py) |

Also included: `screenshots/` (all terminal screenshots) and `reports/` (full pytest output before and after the fix). The original buggy `parking_fee.py` is in the commit history (`Lab-7 (Dhanush): add original parking_fee.py ...`).

## Commands

```bash
pip install hypothesis pytest
python parking_fee.py
python -m pytest test_parking_fee.py
```

## Results

| | Tests passed | Tests failed |
|---|---|---|
| Original (buggy) code | 2 | **8** |
| Fixed code | **10** | 0 |

## Bugs found and fixed

| # | Function | Minimal failing input | Buggy behaviour | Fix |
|---|----------|-----------------------|-----------------|-----|
| 1 | `minutes_parked` | `None` | `AttributeError` | Return `None` for non-strings |
| 2 | `minutes_parked` | `''`, `'-'` | `ValueError` (unpack) | Validate with regex `HH:MM-HH:MM` |
| 3 | `minutes_parked` | `':-:'` | `ValueError` (`int('')`) | Regex accepts only ASCII digits |
| 4 | `minutes_parked` | `'00:01-00:00'` | Returns `-1` | `None` when exit is before entry |
| 5 | `minutes_parked` | `'25:00-26:00'` | Accepts impossible times | Hours 0–23, minutes 0–59 (found by code review) |
| 6 | `hourly_rate` | `None` | `AttributeError` | Return `None` for non-strings |
| 7 | `hourly_rate` | `''`, `'Bus'` | `KeyError` | `RATES.get()` → `None` |
| 8 | `format_plate` | `None` | `AttributeError` | Return `None` for non-strings |
| 9 | `format_plate` | `''` | `IndexError` | Validate before indexing |
| 10 | `format_plate` | `'00'` | Returns `'00   '` | Require `AA00AA0000` (ASCII; spaces/hyphens ignored) |

## Screenshots

| Step | Screenshot |
|------|-----------|
| 2 — buggy program run | [valid input](screenshots/step2_buggy_run_valid.png), [crashes 1](screenshots/step2_buggy_run_crash1.png), [crashes 2](screenshots/step2_buggy_run_crash2.png) |
| 4 — tests failing | [summary](screenshots/step4_tests_failing_summary.png), [errors found](screenshots/step4_tests_failing_bugs_found.png), [minimal examples](screenshots/step4_tests_failing_detail.png) |
| 5 — fixed program run | [valid input](screenshots/step5_fixed_run_valid.png), [bad inputs](screenshots/step5_fixed_run_invalid_inputs.png) |
| 6 — tests passing | [10 passed](screenshots/step6_tests_passing.png) |
