"""Slug generation."""

from validkit._common import require_max_length


def slugify(text: str) -> str:
    require_max_length(text)
    raise NotImplementedError("slugify is not implemented yet")
