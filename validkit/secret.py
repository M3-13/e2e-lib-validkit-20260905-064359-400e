"""Secret masking."""

from validkit._common import require_max_length


def mask_secret(text: str, keep: int = 4) -> str:
    """Mask ``text`` so that only the last ``keep`` characters stay readable.

    Every character outside the trailing ``keep`` characters is replaced with an
    asterisk and the total length is preserved. For ``keep == 0`` the result is
    entirely asterisks, so no character of the input survives. When the input is
    no longer than ``keep`` it is returned unchanged.

    ``keep`` must be a non-negative integer; a negative or non-integer value
    (e.g. a float) raises ``ValueError``. Error messages never contain the input
    value (see AC-15).
    """
    require_max_length(text)
    if not isinstance(keep, int):
        raise ValueError("keep must be a non-negative integer")
    if keep < 0:
        raise ValueError("keep must be a non-negative integer")
    if keep == 0:
        return "*" * len(text)
    if len(text) <= keep:
        return text
    return "*" * (len(text) - keep) + text[-keep:]
