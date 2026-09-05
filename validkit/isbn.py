"""ISBN-13 validation."""

from validkit._common import require_max_length


def is_valid_isbn13(text: str) -> bool:
    require_max_length(text)
    raise NotImplementedError("is_valid_isbn13 is not implemented yet")
