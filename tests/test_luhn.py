"""Tests for validkit.luhn.luhn_check."""

import pytest

from validkit.luhn import luhn_check


def test_valid_card_number_returns_true():
    assert luhn_check("4111111111111111") is True


def test_invalid_check_digit_returns_false():
    assert luhn_check("4111111111111112") is False


def test_digits_with_spaces_and_hyphens():
    assert luhn_check("4111 1111 1111 1111") is True
    assert luhn_check("4111-1111-1111-1111") is True


def test_single_digit_returns_false_without_error():
    assert luhn_check("5") is False


def test_single_zero_is_valid():
    assert luhn_check("0") is True


def test_empty_input_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("")


def test_non_digit_characters_raise_value_error():
    with pytest.raises(ValueError):
        luhn_check("abc")


def test_length_exceeding_max_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("1" * 10001)


def test_error_message_does_not_leak_input():
    with pytest.raises(ValueError) as excinfo:
        luhn_check("abc")
    assert "abc" not in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        luhn_check("")
    assert "''" not in str(excinfo.value)
