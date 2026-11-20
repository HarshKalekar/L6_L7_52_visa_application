"""Decision/branch tests for the Visa Application module (Lab 6)."""
import pytest
from visa_application import visa_fee, documents_complete, application_status


def test_visa_fee_all_decision_outcomes():
    # Unknown/known visa, negative/non-negative entries.
    with pytest.raises(ValueError):
        visa_fee("other", 1, "normal", "B")
    with pytest.raises(ValueError):
        visa_fee("tourist", -1, "normal", "B")

    # Nationality adjustment applies to non-student visas only.
    assert visa_fee("tourist", 2, "normal", "A") == 0
    assert visa_fee("student", 3, "normal", "A") == 40
    assert visa_fee("tourist", 2, "normal", "B") == 40

    # No extra entries, normal/express rate, and >5 extra-entry surcharge.
    assert visa_fee("tourist", 1, "express", "B") == 0
    assert visa_fee("tourist", 2, "express", "B") == 100
    assert visa_fee("tourist", 7, "normal", "B") == 360
    assert visa_fee("tourist", 7, "express", "B") == 780


def test_documents_complete_all_branches():
    assert documents_complete(1, 0, True) is True
    assert documents_complete(0, 4, True) is False
    assert documents_complete(3, 2, False) is True
    assert documents_complete(3, 1, False) is False
    assert documents_complete(2, 2, False) is False


def test_application_status_all_branches():
    # Express and standard cutoffs; peak and non-peak adjustments.
    assert application_status(30, False, False) == "open"
    assert application_status(15, False, False) == "closing"
    assert application_status(14, False, False) == "closed"
    assert application_status(10, True, False) == "open"
    assert application_status(45, False, True) == "open"
    assert application_status(30, False, True) == "closing"
    assert application_status(9, True, True) == "closed"
