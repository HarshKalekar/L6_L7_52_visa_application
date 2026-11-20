"""Property-based fuzz tests for the Visa Application module (Lab 7)."""
import math
import pytest
from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee


# Arbitrary malformed inputs must be rejected predictably, not crash internally.
@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
def test_parse_application_fuzz_no_unexpected_exception(value):
    try:
        result = parse_application(value)
    except ValueError:
        return
    assert isinstance(value, str)
    assert isinstance(result, tuple) and len(result) == 2
    assert isinstance(result[0], str) and result[0]
    assert isinstance(result[1], int) and result[1] >= 0


@given(st.text())
def test_processing_average_fuzz_no_unexpected_exception(value):
    try:
        result = processing_average(value)
    except ValueError:
        return
    assert isinstance(result, int) and result >= 0


@given(st.one_of(st.text(), st.none(), st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
def test_payable_fee_fuzz_no_unexpected_exception(value):
    try:
        result = payable_fee(value)
    except ValueError:
        return
    assert isinstance(result, float) and math.isfinite(result) and result >= 0


# Valid-input properties verify the calculations as well as robustness.
@given(st.text(alphabet=st.characters(blacklist_characters=":"), min_size=1).map(str.strip).filter(bool),
       st.integers(min_value=0, max_value=100000))
def test_parse_application_valid_inputs(visa_type, entries):
    parsed_type, parsed_entries = parse_application(f" {visa_type} : {entries} ")
    assert parsed_type == visa_type.strip().title()
    assert parsed_entries == entries


@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=1, max_size=100))
def test_processing_average_valid_inputs(days):
    csv = ",".join(map(str, days))
    assert processing_average(csv) == sum(days) // len(days)


@given(st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False),
       st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False))
def test_payable_fee_valid_inputs(fee, discount):
    expected = max(fee * 1.18 - discount, 0.0)
    assert payable_fee(f"{fee}|{discount}") == pytest.approx(expected)


@pytest.mark.parametrize("value", [None, 1, "", ":2", "tourist:", "tourist:1:2", "tourist:-1", "tourist:two"])
def test_parse_application_invalid_examples(value):
    with pytest.raises(ValueError):
        parse_application(value)


@pytest.mark.parametrize("value", [None, "", ",", "1,", ",2", "1,,2", "1,-2", "1,x"])
def test_processing_average_invalid_examples(value):
    with pytest.raises(ValueError):
        processing_average(value)


@pytest.mark.parametrize("value", [None, "", "100", "|5", "100|", "1|2|3", "x|2", "NaN|0", "Infinity|0", "-1|0", "1|-2"])
def test_payable_fee_invalid_examples(value):
    with pytest.raises(ValueError):
        payable_fee(value)


def test_payable_fee_discount_cannot_make_negative_total():
    assert payable_fee("100|1000") == 0.0
