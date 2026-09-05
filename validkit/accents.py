"""Diacritics removal."""

from validkit._common import require_max_length


def strip_accents(text: str) -> str:
    require_max_length(text)
    raise NotImplementedError("strip_accents is not implemented yet")
