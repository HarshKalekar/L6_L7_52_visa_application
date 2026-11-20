"""Line-coverage tests for the Visa Application module (Lab 6)."""
import pytest
from visa_application import visa_fee, documents_complete, application_status


@pytest.mark.parametrize(
    "visa_type,entries,speed,nationality,expected",
    [
        ("tourist", 1, "normal", "B", 0),
        ("business", 3, "normal", "B", 0),
        ("student", 2, "normal", "A", 0),
        ("tourist", 3, "normal", "A", 40),
        ("tourist", 2, "express", "B", 100),
        ("business", 10, "express", "B", 910),
        ("business", 10, "normal", "B", 420),
    ],
)
def test_visa_fee_valid_scenarios(visa_type, entries, speed, nationality, expected):
    assert visa_fee(visa_type, entries, speed, nationality) == expected


def test_visa_fee_unknown_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "normal", "B")


def test_visa_fee_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_documents_complete_renewal_true_and_false():
    assert documents_complete(1, 0, True) is True
    assert documents_complete(0, 5, True) is False


def test_documents_complete_new_application_photo_and_form_rules():
    assert documents_complete(3, 2, False) is True
    assert documents_complete(5, 1, False) is False
    assert documents_complete(2, 2, False) is False


def test_application_status_open_closing_closed():
    assert application_status(30, False, False) == "open"
    assert application_status(20, False, False) == "closing"
    assert application_status(14, False, False) == "closed"


def test_application_status_express_and_peak_season():
    assert application_status(10, True, False) == "open"
    assert application_status(30, False, True) == "closing"
    assert application_status(15, True, True) == "closing"
