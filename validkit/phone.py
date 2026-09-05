"""Phone number normalization to E.164."""

from typing import Union

from validkit._common import require_max_length

# typing.Union is required by the binding contract (Python >= 3.9): the PEP 604
# ``X | Y`` syntax that UP007 suggests evaluates at import time and raises
# TypeError on 3.9, breaking ``import validkit``. UP007 is a false positive here
# because the office ruff.toml pins target-version = "py313".


def normalize_phone(text: str, country_code: Union[str, int]) -> str:  # noqa: UP007
    require_max_length(text)
    raise NotImplementedError("normalize_phone is not implemented yet")
