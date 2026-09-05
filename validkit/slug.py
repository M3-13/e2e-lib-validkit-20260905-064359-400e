"""Slug generation."""

import re
import unicodedata

from validkit._common import require_max_length


def slugify(text: str) -> str:
    """Turn ``text`` into a URL-friendly slug.

    Lowercases the input, strips umlauts/diacritics by NFKD-normalizing and
    dropping combining characters, replaces every run of non-word characters
    with a single ``-`` and finally trims leading/trailing ``-``.
    """
    require_max_length(text)
    normalized = unicodedata.normalize("NFKD", text.lower())
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\W+", "-", ascii_text).strip("-")
