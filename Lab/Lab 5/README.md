# Lab 5: Static Code Analysis — Library Fine and Book Renewal System

**Student:** C Rohit Reddy  
**SRN:** PES2UG24CS125  
**Course:** Software Engineering (SETA Labs)  
**File Under Analysis:** `library_system.py`  

---

## Overview

Lab 5 applies industry-standard static analysis and linting tools to audit and remediate bugs, anti-patterns, style violations, and security flaws:
- **Flake8**: Enforces PEP 8 style guide, layout, and common syntax issues.
- **Pylint**: Analyzes code quality, dangerous defaults, missing docstrings, and refactoring candidates.
- **Bandit**: Scans for Common Weakness Enumeration (CWE) vulnerabilities (e.g. insecure `eval()`, bare exception suppression).

## Inspection Results Summary

| Metric / Tool | Initial Score / Issues | Remediated Score / Issues |
|:---|:---:|:---:|
| **Pylint** | **6.07 / 10** | **10.00 / 10** |
| **Bandit** | **2 Issues** (1 Medium B307, 1 Low B110) | **0 Issues** (No issues identified) |
| **Flake8** | **14 Violations** | **0 Violations** |

## Files in Directory
- `library_system.py`: Fully remediated and hardened library management script.
- `bandit_report_before.txt` & `bandit_report_after.txt`: Security scan before and after fixes.
- `pylint_report_before.txt` & `pylint_report_after.txt`: Pylint code rating progression from 6.07 to 10.00.
- `flake8_report_before.txt` & `flake8_report_after.txt`: PEP 8 compliance logs.
- `issues.md`: Detailed catalog of all detected bugs, CWEs, and remediation steps.
- `reflection.md`: In-depth reflection answering analytical questions on tooling efficacy.
