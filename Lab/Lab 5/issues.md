# Lab 5: Static Analysis Issues & Remediation

| Issue | Tool & Category | Line(s) | Description | Fix Approach |
|:------|:----------------|:-------:|:------------|:-------------|
| **Insecure `eval()` Usage** | Bandit B307 / Security | 45 | `eval(rule.replace('days', str(days)))` permits arbitrary code execution if rule is unvalidated. | Replaced with deterministic arithmetic evaluation `fine_from_rule(rate_per_day, days)`. |
| **Bare `except: pass`** | Bandit B110 & Pylint W0702 | 21 | Silent suppression of all runtime exceptions masks programming errors and key errors. | Removed bare try/except block; implemented explicit key presence checks with `dict.get()`. |
| **Dangerous Default Mutable Argument** | Pylint W0102 | 9 | `def issue_book(..., tags=[])` uses mutable default list shared across all calls. | Changed default to `tags=None` and initialized `tags = []` inside the function body. |
| **Unclosed File Descriptors & Missing Encoding** | Pylint W1514 & R1732 | 34, 40 | `open()` without `with` statement risks resource leakage; missing explicit UTF-8 encoding. | Wrapped file access in `with open(LOANS_FILE, 'r'/'w', encoding='utf-8') as f:`. |
| **Non-Standard Naming Convention** | Pylint C0103 | 27 | `renewBook` violated PEP 8 `snake_case` convention. | Renamed function to `renew_book`. |
| **Missing Module & Function Docstrings** | Pylint C0114 & C0116 | Multiple | All functions lacked PEP 257 docstrings. | Added comprehensive docstrings to module header and every function definition. |
| **Unused Import** | Flake8 F401 & Pylint W0611 | 2 | `import os` was never used. | Removed unused import. |
| **Excessive Line Length** | Flake8 E501 | 14, 31 | Lines exceeded 79 characters. | Refactored string formatting and broke lines within PEP 8 limits. |
