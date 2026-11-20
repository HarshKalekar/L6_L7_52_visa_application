# L6_L7_52 — Visa Application

## Lab 7: Hypothesis Fuzz Testing

- `visa_application.py` — validated application parsing, processing-day averaging, and fee calculation.
- `test_visa_application.py` — Hypothesis property-based fuzz tests plus explicit malformed-input regression tests.

Install dependencies and run from this directory:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Malformed or unsupported inputs are rejected with `ValueError`; valid values are checked against calculation properties. Hypothesis generates additional examples and shrinks failures to minimal counterexamples.
