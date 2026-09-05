"""Public API surface of validkit.

This test file is owned by the package-skeleton ticket. It asserts only what the
skeleton itself delivers: the nine names are importable, ``__all__`` is complete,
the stub signatures match the sprint contract, and the shared length guard
behaves correctly. It deliberately does NOT assert the *results* of the nine
functions — those are the responsibility of the feature tickets.
"""

import inspect

import pytest

import validkit
from validkit._common import require_max_length

ALL_NAMES = [
    "clamp",
    "is_valid_email",
    "is_valid_iban",
    "is_valid_isbn13",
    "luhn_check",
    "mask_secret",
    "normalize_phone",
    "slugify",
    "strip_accents",
]

EXPECTED_PARAMS = {
    "is_valid_email": ["text"],
    "luhn_check": ["digits"],
    "is_valid_iban": ["text"],
    "is_valid_isbn13": ["text"],
    "normalize_phone": ["text", "country_code"],
    "strip_accents": ["text"],
    "mask_secret": ["text", "keep"],
    "slugify": ["text"],
    "clamp": ["value", "low", "high"],
}


def test_all_names_are_importable():
    for name in ALL_NAMES:
        assert hasattr(validkit, name), f"{name} is not exported"
        assert getattr(validkit, name) is not None


def test_all_contains_exactly_the_nine_names():
    assert set(validkit.__all__) == set(ALL_NAMES)
    assert len(validkit.__all__) == len(ALL_NAMES)


def test_stub_signatures_match_the_contract():
    for name, params in EXPECTED_PARAMS.items():
        fn = getattr(validkit, name)
        sig = inspect.signature(fn)
        assert list(sig.parameters) == params, f"{name} has wrong parameters"


def test_mask_secret_keep_default_is_four():
    sig = inspect.signature(validkit.mask_secret)
    assert sig.parameters["keep"].default == 4


def test_annotations_use_typing_union_not_pep604():
    for name in ALL_NAMES:
        fn = getattr(validkit, name)
        sig = inspect.signature(fn)
        for param in sig.parameters.values():
            assert "|" not in str(param.annotation), (
                f"{name}.{param.name} uses `X | Y` syntax; use typing.Union"
            )
        if sig.return_annotation is not inspect.Signature.empty:
            assert "|" not in str(sig.return_annotation), (
                f"{name} return annotation uses `X | Y` syntax; use typing.Union"
            )


def test_require_max_length_raises_above_limit():
    with pytest.raises(ValueError):
        require_max_length("x" * 10001)


def test_require_max_length_allows_at_or_below_limit():
    require_max_length("")
    require_max_length("x" * 10000)


def test_require_max_length_message_does_not_leak_input():
    secret = "x" * 10001
    with pytest.raises(ValueError) as excinfo:
        require_max_length(secret)
    assert secret not in str(excinfo.value)
