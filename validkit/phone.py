"""Phone number normalization to E.164."""

from typing import Union

from validkit._common import require_max_length

# typing.Union is required by the binding contract (Python >= 3.9): the PEP 604
# ``X | Y`` syntax that UP007 suggests evaluates at import time and raises
# TypeError on 3.9, breaking ``import validkit``. UP007 is a false positive here
# because the office ruff.toml pins target-version = "py313".


def normalize_phone(text: str, country_code: Union[str, int]) -> str:  # noqa: UP007
    """Normalize ``text`` into an E.164 phone number.

    Separators (spaces, parentheses and hyphens) are removed first. A leading
    ``+`` or ``00`` marks an international number whose country code is already
    embedded; a leading ``0`` marks a national number whose trunk prefix is
    replaced by ``country_code``. A number with no such prefix is treated as a
    national number without a trunk prefix, so ``country_code`` is prepended.

    Returns ``+<country_code><subscriber digits>`` with no separators. Raises
    ``ValueError`` for inputs that carry no interpretable digits (empty, or no
    digits at all). Error messages never contain the input value (see AC-15).
    """
    require_max_length(text)
    cc = _country_code_digits(country_code)

    cleaned = text.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")

    if not cleaned:
        raise ValueError("phone number is empty")

    if cleaned.startswith("+"):
        digits = cleaned[1:]
    elif cleaned.startswith("00"):
        digits = cleaned[2:]
    elif cleaned.startswith("0"):
        digits = cc + cleaned[1:]
    else:
        digits = cc + cleaned

    if not digits:
        raise ValueError("phone number has no subscriber digits")
    if not digits.isdigit():
        raise ValueError("phone number contains characters that are not digits")

    return "+" + digits


def _country_code_digits(country_code: Union[str, int]) -> str:  # noqa: UP007
    cc = str(country_code).strip()
    if not cc:
        raise ValueError("country code is empty")
    if not cc.isdigit():
        raise ValueError("country code must contain only digits")
    return cc
