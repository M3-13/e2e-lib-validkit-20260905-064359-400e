"""Tests for IBAN validation."""

import pytest

from validkit.iban import is_valid_iban


def test_valid_iban_plain():
    assert is_valid_iban("DE89370400440532013000") is True


def test_valid_iban_with_spaces():
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_valid_iban_lowercase():
    assert is_valid_iban("de89370400440532013000") is True


def test_valid_iban_other_country():
    assert is_valid_iban("GB29 NWBK 6016 1331 9268 19") is True
    assert is_valid_iban("CH9300762011623852957") is True


def test_manipulated_checksum_returns_false():
    assert is_valid_iban("DE88370400440532013000") is False


def test_wrong_checksum_with_spaces_returns_false():
    assert is_valid_iban("DE89 3704 0044 0532 0130 01") is False


def test_unknown_country_code_returns_false():
    assert is_valid_iban("ZZ89370400440532013000") is False


def test_wrong_length_returns_false():
    assert is_valid_iban("DE8937040044053201300") is False


def test_non_alphanumeric_returns_false():
    assert is_valid_iban("DE89-3704-0044-0532-0130-00") is False


def test_empty_input_returns_false():
    assert is_valid_iban("") is False


def test_over_max_length_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_iban("DE" + "A" * 10000)
