"""Value clamping into an inclusive range."""

from typing import Union

# typing.Union is required by the binding contract (Python >= 3.9): the PEP 604
# ``X | Y`` syntax that UP007 suggests evaluates at import time and raises
# TypeError on 3.9, breaking ``import validkit``. UP007 is a false positive here
# because the office ruff.toml pins target-version = "py313".


def clamp(
    value: Union[int, float],  # noqa: UP007
    low: Union[int, float],  # noqa: UP007
    high: Union[int, float],  # noqa: UP007
) -> Union[int, float]:  # noqa: UP007
    """Clamp ``value`` into the inclusive range ``[low, high]``.

    Returns ``min(max(value, low), high)`` so ``int`` and ``float`` inputs keep
    their type (no forced cast). Raises ``ValueError`` when ``low > high``; the
    message deliberately does not echo the input values (see AC-15).
    """
    if low > high:
        raise ValueError("low must not be greater than high")
    return min(max(value, low), high)
