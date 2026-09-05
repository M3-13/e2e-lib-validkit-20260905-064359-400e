"""Shared helpers used across the validkit modules."""

_DEFAULT_MAX_LENGTH = 10000


def require_max_length(value: str, max_length: int = _DEFAULT_MAX_LENGTH) -> None:
    """Reject inputs above a documented maximum length before any real validation.

    Raises ``ValueError`` when ``len(value) > max_length``. The message is
    deliberately context-free of the offending input value (see AC-15) to avoid
    leaking user data into logs or error reports.
    """
    if len(value) > max_length:
        raise ValueError(f"input exceeds the maximum allowed length of {max_length} characters")
