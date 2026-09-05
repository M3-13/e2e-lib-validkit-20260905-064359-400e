"""Tests for ``validkit.phone.normalize_phone``."""

import pytest

from validkit.phone import normalize_phone


def test_normalize_international_plus_number():
    assert normalize_phone("+49 170 1234567", "49") == "+491701234567"


def test_normalize_removes_parentheses_and_hyphens():
    assert normalize_phone("+49 (170) 123-4567", "49") == "+491701234567"


def test_normalize_international_00_prefix():
    assert normalize_phone("0049 170 1234567", "49") == "+491701234567"


def test_normalize_national_leading_zero_is_replaced_by_country_code():
    assert normalize_phone("0170 1234567", "49") == "+491701234567"


def test_normalize_national_without_prefix_prepends_country_code():
    assert normalize_phone("170 1234567", "49") == "+491701234567"


def test_normalize_accepts_int_country_code():
    assert normalize_phone("0170 1234567", 49) == "+491701234567"
    assert normalize_phone("+49 170 1234567", 49) == "+491701234567"


def test_normalize_empty_input_raises():
    with pytest.raises(ValueError):
        normalize_phone("", "49")


def test_normalize_whitespace_only_input_raises():
    with pytest.raises(ValueError):
        normalize_phone("   ", "49")


def test_normalize_letters_only_input_raises():
    with pytest.raises(ValueError):
        normalize_phone("abc", "49")


def test_normalize_plus_without_digits_raises():
    with pytest.raises(ValueError):
        normalize_phone("+", "49")


def test_normalize_input_exceeding_max_length_raises():
    with pytest.raises(ValueError):
        normalize_phone("x" * 10001, "49")


def test_normalize_error_messages_do_not_leak_input():
    secret = "0170 1234567"
    with pytest.raises(ValueError) as excinfo:
        normalize_phone(secret, "not-a-code")
    assert secret not in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        normalize_phone("abc", "49")
    assert "abc" not in str(excinfo.value)


def test_normalize_empty_country_code_raises():
    with pytest.raises(ValueError):
        normalize_phone("0170 1234567", "")


def test_normalize_invalid_country_code_raises():
    with pytest.raises(ValueError):
        normalize_phone("0170 1234567", "4a")
