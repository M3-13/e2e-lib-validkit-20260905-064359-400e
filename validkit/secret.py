"""Secret masking."""

from validkit._common import require_max_length


def mask_secret(text: str, keep: int = 4) -> str:
    require_max_length(text)
    raise NotImplementedError("mask_secret is not implemented yet")
