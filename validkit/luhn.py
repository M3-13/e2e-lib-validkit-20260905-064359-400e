"""Luhn checksum validation."""

from validkit._common import require_max_length


def luhn_check(digits: str) -> bool:
    """Return True if ``digits`` is a valid Luhn number.

    The input may contain spaces and hyphens, which are ignored. The check
    digit (the rightmost digit) is validated by doubling every second digit
    from the right and summing the digits of each doubled value. Raises
    ``ValueError`` for empty input or any character that is not a digit.
    """
    require_max_length(digits)

    cleaned = digits.replace(" ", "").replace("-", "")
    if not cleaned:
        raise ValueError("input must contain at least one digit")
    if not cleaned.isdigit():
        raise ValueError("input must contain only digits")

    total = 0
    for index, char in enumerate(reversed(cleaned)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value

    return total % 10 == 0
