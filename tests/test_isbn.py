"""Tests for ISBN-13 validation."""

import pytest

from validkit.isbn import is_valid_isbn13


def test_valid_isbn13_with_hyphens():
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_valid_isbn13_without_separators():
    assert is_valid_isbn13("9783161484100") is True


def test_valid_isbn13_with_spaces():
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_second_valid_isbn13():
    assert is_valid_isbn13("978-0-306-40615-7") is True


def test_wrong_check_digit_returns_false():
    assert is_valid_isbn13("978-3-16-148410-1") is False


def test_too_short_returns_false():
    assert is_valid_isbn13("978-3-16-148410") is False


def test_too_long_returns_false():
    assert is_valid_isbn13("978-3-16-148410-00") is False


def test_non_digit_returns_false():
    assert is_valid_isbn13("978-3-16-148410-X") is False


def test_empty_returns_false():
    assert is_valid_isbn13("") is False


def test_only_separators_returns_false():
    assert is_valid_isbn13("---   ") is False


def test_length_above_limit_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_isbn13("9" * 10001)


def test_length_at_limit_does_not_raise():
    assert is_valid_isbn13("9" * 10000) is False
