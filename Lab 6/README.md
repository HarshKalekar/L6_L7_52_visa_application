# L6_L7_52 — Visa Application

## Lab 6: Code and Branch Coverage

Application module: `visa_application.py`  
Coverage test suites:
- `CodeCoverageTest_visa_application.py` — broad line/function coverage.
- `BranchCoverageTest_visa_application.py` — exercises both outcomes of each decision.

Install and run from this directory:

```bash
python -m pip install pytest coverage
coverage erase
coverage run -m pytest -q CodeCoverageTest_visa_application.py
coverage report -m visa_application.py
coverage erase
coverage run --branch -m pytest -q BranchCoverageTest_visa_application.py
coverage report -m visa_application.py
```

The starter `test_visa_application.py` is retained for reference. The two named suites above are the submission test files.
