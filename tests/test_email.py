"""Tests for e-mail address validation."""

import pytest

from validkit.email import is_valid_email


def test_valid_email_returns_true():
    assert is_valid_email("test@example.com") is True


def test_valid_email_with_dot_in_local_part():
    assert is_valid_email("first.last@example.com") is True


def test_valid_email_with_plus_tag():
    assert is_valid_email("user+tag@example.com") is True


def test_valid_email_with_subdomain():
    assert is_valid_email("user@sub.example.co.uk") is True


def test_missing_at_returns_false():
    assert is_valid_email("not-an-email") is False


def test_empty_string_returns_false():
    assert is_valid_email("") is False


def test_missing_domain_returns_false():
    assert is_valid_email("test@") is False


def test_missing_local_part_returns_false():
    assert is_valid_email("@example.com") is False


def test_invalid_domain_returns_false():
    assert is_valid_email("test@.com") is False
    assert is_valid_email("test@example.") is False


def test_domain_without_dot_returns_false():
    assert is_valid_email("test@example") is False


def test_space_in_address_returns_false():
    assert is_valid_email("test @example.com") is False


def test_invalid_input_returns_false_not_exception():
    assert is_valid_email("not-an-email") is False


def test_over_max_length_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_email("a" * 10001 + "@example.com")


def test_exactly_max_length_does_not_raise():
    assert is_valid_email("a" * 9988 + "@example.com") is True
