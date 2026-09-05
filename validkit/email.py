"""E-mail address validation."""

from validkit._common import require_max_length


def is_valid_email(text: str) -> bool:
    require_max_length(text)
    raise NotImplementedError("is_valid_email is not implemented yet")
