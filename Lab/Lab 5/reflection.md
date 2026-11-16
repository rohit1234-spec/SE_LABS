# Lab 5: Reflection on Static Code Analysis

## 1. Which issues were easiest and hardest to fix?
- **Easiest:** Eliminating unused imports (`os`), renaming `renewBook` to `renew_book`, formatting docstrings, and wrapping file I/O operations inside `with` context managers.
- **Hardest:** Addressing Bandit's security warning regarding dynamic formula evaluation (`eval()`). Simply replacing `eval` required rethinking the API contract of `fine_from_rule` to parse numeric rates safely without compromising mathematical precision or exposing the runtime to arbitrary expression execution.

## 2. Did the tools report anything wrong or unhelpful?
- Pylint's warning on global variable usage (`W0603`) in small administrative scripts is often noisy, though valid for large applications. In production code, encapsulating state inside a `LibrarySystem` class is cleaner than global module-level dictionaries.
- Flake8 is strict on whitespace and 79-character column limits (E501), which can occasionally force awkward line continuations in modern widescreen environments, but ensures high consistency across collaborative codebases.

## 3. How do static analysis tools complement testing?
Static analysis operates without executing the software, discovering edge-case defects (e.g. mutable default arguments, security vulnerabilities, unclosed file descriptors) that typical test suites might never trigger during regular execution paths.
