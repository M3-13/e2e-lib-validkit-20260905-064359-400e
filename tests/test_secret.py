"""Tests for ``validkit.secret.mask_secret``."""

import pytest

from validkit.secret import mask_secret


def test_mask_secret_keeps_last_keep_characters():
    assert mask_secret("geheim123", keep=3) == "******123"


def test_mask_secret_default_keep_is_four():
    assert mask_secret("geheim123") == "*****m123"


def test_mask_secret_preserves_length():
    result = mask_secret("geheim123", keep=3)
    assert len(result) == len("geheim123")


def test_mask_secret_keep_zero_masks_everything():
    result = mask_secret("geheim123", keep=0)
    assert result == "*" * 9
    assert len(result) == 9


def test_mask_secret_keep_zero_leaks_nothing():
    secret = "geheim123"
    result = mask_secret(secret, keep=0)
    for char in secret:
        assert char not in result


def test_mask_secret_keep_equals_length_returns_unchanged():
    assert mask_secret("geheim123", keep=9) == "geheim123"


def test_mask_secret_text_shorter_than_keep_returns_unchanged():
    assert mask_secret("abc", keep=10) == "abc"


def test_mask_secret_empty_input():
    assert mask_secret("", keep=4) == ""
    assert mask_secret("", keep=0) == ""


def test_mask_secret_negative_keep_raises():
    with pytest.raises(ValueError):
        mask_secret("geheim123", keep=-1)


def test_mask_secret_float_keep_raises():
    with pytest.raises(ValueError):
        mask_secret("geheim123", keep=3.0)


def test_mask_secret_error_message_does_not_leak_input():
    secret = "geheim123"
    with pytest.raises(ValueError) as excinfo:
        mask_secret(secret, keep=-2)
    assert secret not in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        mask_secret(secret, keep=2.5)
    assert secret not in str(excinfo.value)
