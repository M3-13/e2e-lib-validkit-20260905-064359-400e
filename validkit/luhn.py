"""Luhn checksum validation."""

from validkit._common import require_max_length


def luhn_check(digits: str) -> bool:
    require_max_length(digits)
    raise NotImplementedError("luhn_check is not implemented yet")
