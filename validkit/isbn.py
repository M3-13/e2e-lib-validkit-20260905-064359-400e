"""ISBN-13 validation."""

from validkit._common import require_max_length


def is_valid_isbn13(text: str) -> bool:
    """Return True if ``text`` is a valid ISBN-13, otherwise False.

    Leading/trailing and internal spaces and hyphens are ignored. The value must
    consist of exactly 13 digits after that normalization, and its check digit
    must satisfy the 1/3-weighted checksum (sum modulo 10 == 0).

    Returns ``False`` for a wrong length or a wrong check digit; raises
    ``ValueError`` only when the input exceeds the documented maximum length
    (see ``require_max_length``).
    """
    require_max_length(text)
    cleaned = text.replace(" ", "").replace("-", "")
    if len(cleaned) != 13 or not cleaned.isdigit():
        return False
    total = sum(int(digit) * (1 if index % 2 == 0 else 3) for index, digit in enumerate(cleaned))
    return total % 10 == 0
