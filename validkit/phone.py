"""Phone number normalization to E.164."""

from validkit._common import require_max_length


def normalize_phone(text: str, country_code: str | int) -> str:
    require_max_length(text)
    raise NotImplementedError("normalize_phone is not implemented yet")
