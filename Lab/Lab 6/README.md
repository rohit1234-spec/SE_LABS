# Lab 6: Dynamic White-Box Testing & Code Coverage

**Student:** C Rohit Reddy  
**SRN:** PES2UG24CS125  
**Course:** Software Engineering (SETA Labs)  
**Module Under Test:** `water_utility_billing.py`  

---

## Overview

Lab 6 focuses on dynamic unit testing, control-flow path analysis, and achieving **100% Line Coverage** and **100% Branch Coverage** using **Pytest** and the Python **Coverage** library.

### Module Functionality (`water_utility_billing.py`):
1. **`calculate_water_bill(accounts, base_fee)`**:
   - Computes tiered billing across residential and commercial accounts based on usage blocks.
   - Applies leak waiver deductions for accounts exceeding bill thresholds.
   - Evaluates system operational flags (`NORMAL`, `NO_ACTIVITY`, `EXCESSIVE_FLAGS`).
2. **`check_meter_tampering(readings_matrix)`**:
   - Analyzes consumption reading delta matrices across multiple meters.
   - Detects negative deltas indicative of reverse-flow tampering (`TAMPER_SUSPECTED`, `CLEAR`, `NO_DATA`).

---

## Coverage Analysis Results

```
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
water_utility_billing.py      43      0     32      0   100%
----------------------------------------------------------------------
TOTAL                         43      0     32      0   100%
```

- **Total Test Cases Executed:** 32 Passed
- **Statement (Line) Coverage:** **100%** (43 / 43 statements)
- **Branch Coverage:** **100%** (32 / 32 branches evaluated in all binary outcomes)

---

## Artifacts & Deliverables
- `water_utility_billing.py`: Core production business logic module.
- `CodeCoverageTest_water_utility_billing.py`: Targeted unit tests achieving 100% statement coverage.
- `BranchCoverageTest_water_utility_billing.py`: Comprehensive branch coverage test cases covering all edge conditions.
- `code_coverage_report.png`: Terminal execution screenshot verifying 100% line coverage.
- `branch_coverage_report.png`: Terminal execution screenshot verifying 100% branch coverage.
- `commits_history.png`: Git version control commit timeline screenshot.
- `submissions/`: PDF reports and test scripts submitted for academic evaluation.
