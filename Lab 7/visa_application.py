"""Input parsing and fee calculations for visa applications."""
import math


def parse_application(text):
    """Parse 'visa_type:entries' and return (title-cased type, entry count).

    Raises ValueError for malformed input, empty visa types, or negative entries.
    """
    if not isinstance(text, str):
        raise ValueError("application must be a string")
    if text.count(":") != 1:
        raise ValueError("application must contain exactly one ':' separator")
    visa, entries_text = text.split(":")
    visa = visa.strip()
    entries_text = entries_text.strip()
    if not visa:
        raise ValueError("visa type cannot be empty")
    if not entries_text:
        raise ValueError("entries cannot be empty")
    try:
        entries = int(entries_text)
    except (TypeError, ValueError) as exc:
        raise ValueError("entries must be an integer") from exc
    if entries < 0:
        raise ValueError("entries cannot be negative")
    return visa.title(), entries


def processing_average(days_csv):
    """Return the floor average of a non-empty CSV list of non-negative days."""
    if not isinstance(days_csv, str):
        raise ValueError("processing days must be a string")
    parts = days_csv.split(",")
    if not parts or any(not part.strip() for part in parts):
        raise ValueError("processing days must be a non-empty comma-separated list")
    try:
        values = [int(part.strip()) for part in parts]
    except ValueError as exc:
        raise ValueError("each processing day must be an integer") from exc
    if any(value < 0 for value in values):
        raise ValueError("processing days cannot be negative")
    return sum(values) // len(values)


def payable_fee(text):
    """Calculate max(fee * 1.18 - discount, 0) from 'fee|discount'."""
    if not isinstance(text, str):
        raise ValueError("fee input must be a string")
    if text.count("|") != 1:
        raise ValueError("fee input must contain exactly one '|' separator")
    fee_text, discount_text = (part.strip() for part in text.split("|"))
    if not fee_text or not discount_text:
        raise ValueError("fee and discount are required")
    try:
        fee = float(fee_text)
        discount = float(discount_text)
    except ValueError as exc:
        raise ValueError("fee and discount must be numeric") from exc
    if not math.isfinite(fee) or not math.isfinite(discount):
        raise ValueError("fee and discount must be finite numbers")
    if fee < 0 or discount < 0:
        raise ValueError("fee and discount cannot be negative")
    return max(fee * 1.18 - discount, 0.0)


def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    print("Visa Type and Entries:", parse_application(user_input))
    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    print("Average Processing Days:", processing_average(user_input))
    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    print("Payable Fee:", payable_fee(user_input))


if __name__ == "__main__":
    main()
