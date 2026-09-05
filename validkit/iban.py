"""IBAN validation via modulo-97 checksum."""

from validkit._common import require_max_length

# IBAN lengths for a set of common countries. An IBAN whose country code is not
# listed here (or whose length does not match) is rejected as structurally
# invalid.
_IBAN_LENGTHS = {
    "AD": 24,
    "AT": 20,
    "BE": 16,
    "CH": 21,
    "CZ": 24,
    "DE": 22,
    "DK": 18,
    "EE": 20,
    "ES": 24,
    "FI": 18,
    "FR": 27,
    "GB": 22,
    "GR": 27,
    "HR": 21,
    "HU": 28,
    "IE": 22,
    "IS": 26,
    "IT": 27,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "LV": 21,
    "MC": 27,
    "MT": 31,
    "NL": 18,
    "NO": 15,
    "PL": 28,
    "PT": 25,
    "RO": 24,
    "SE": 24,
    "SI": 19,
    "SK": 24,
}


def _mod_97(rearranged: str) -> int:
    """Compute the value of the IBAN digit sequence modulo 97.

    Letters are mapped to their numeric equivalents (A=10 .. Z=35) and the
    remainder is accumulated incrementally to avoid building an oversized
    intermediate integer.
    """
    remainder = 0
    for char in rearranged:
        if char.isdigit():
            remainder = (remainder * 10 + int(char)) % 97
        else:
            remainder = (remainder * 100 + (ord(char) - 55)) % 97
    return remainder


def is_valid_iban(text: str) -> bool:
    """Return True when ``text`` is a structurally and checksum-valid IBAN.

    Spaces are ignored and case is normalized before validation. A structurally
    invalid IBAN (unknown country code, wrong length, non-alphanumeric
    characters) or a wrong checksum returns False rather than raising.
    """
    require_max_length(text)

    normalized = text.replace(" ", "").upper()

    if not normalized.isalnum():
        return False

    country_code = normalized[:2]
    expected_length = _IBAN_LENGTHS.get(country_code)
    if expected_length is None:
        return False
    if len(normalized) != expected_length:
        return False
    if not normalized[2:4].isdigit():
        return False

    rearranged = normalized[4:] + normalized[:4]
    return _mod_97(rearranged) == 1
