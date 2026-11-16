# Lab 7: Property-Based Fuzz Testing with Hypothesis

**Student:** C Rohit Reddy  
**SRN:** PES2UG24CS125  
**Section:** 5C  
**Course:** Software Engineering (SETA Labs)  
**Submission Document:** [Lab_07_PES2UG24CS125.pdf](./Lab_07_PES2UG24CS125.pdf)  

---

## Overview

Lab 7 explores dynamic property-based fuzz testing as a software security and robustness technique using Python's **Hypothesis** framework. We analyze input validation vulnerabilities and harden three utility billing functions against malicious and malformed data:
1. `sanitize_meter_id(meter_id)`
2. `parse_consumption_readings(readings_csv)`
3. `format_billing_summary(account_record)`

---

## Vulnerabilities Discovered & Hardening

| Function | Fuzzing Trigger | Defect / Failure Type | Hardening Resolution |
|:---|:---|:---|:---|
| **`sanitize_meter_id`** | `s = None`, non-string types | `AttributeError: 'NoneType' object has no attribute 'strip'` | Added `if meter_id is None or not isinstance(meter_id, str): return ""` |
| **`parse_consumption_readings`** | Non-numeric entries, empty tokens, `None` | `ValueError: invalid literal for int() with base 10` | Implemented per-token `try/except (ValueError, TypeError)` filtering; discards invalid tokens safely |
| **`format_billing_summary`** | Truncated records, non-integer usage | `IndexError: list index out of range`, `ValueError` | Validates delimiter split length `>= 3`, type-guards unit conversion, returns `"Invalid account record"` on malformed input |

---

## Verification

Running Hypothesis fuzzing across arbitrary input strategies (`st.text() | st.none()`):
```bash
pytest test_processor.py
```
**Result:** 100% tests passed without unhandled exceptions or crashes.

---

## Files in Directory
- `processor.py`: Hardened, production-ready implementation.
- `processor_buggy.py`: Unhardened starter code demonstrating original fuzz vulnerabilities.
- `test_processor.py`: Property-based Hypothesis fuzz test suite.
- `Lab_07_PES2UG24CS125.pdf`: Formal academic submission document.
- `hypothesis_fuzzing_failures.png`: Terminal capture showing initial hypothesis test crash traces.
- `hypothesis_tests_passing.png`: Terminal capture showing 100% passing tests post-remediation.
- `screenshots/`: Ordered step-by-step verification captures.
