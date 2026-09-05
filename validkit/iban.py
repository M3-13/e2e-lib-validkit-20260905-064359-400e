"""IBAN validation via modulo-97."""

from validkit._common import require_max_length


def is_valid_iban(text: str) -> bool:
    require_max_length(text)
    raise NotImplementedError("is_valid_iban is not implemented yet")
