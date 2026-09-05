"""Diacritics removal."""

import unicodedata

from validkit._common import require_max_length


def strip_accents(text: str) -> str:
    """Return ``text`` with diacritical marks removed.

    The input is normalized with ``unicodedata.normalize('NFKD', ...)`` and every
    non-spacing combining mark (Unicode category ``Mn``) is then dropped. All
    other characters — including spacing combining marks and the base letters
    themselves — are left unchanged. The length guard runs first, so inputs
    longer than the documented maximum raise ``ValueError`` without the input
    value appearing in the message (see AC-15).
    """
    require_max_length(text)
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")
