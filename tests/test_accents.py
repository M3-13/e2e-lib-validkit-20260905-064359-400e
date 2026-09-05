"""Tests for ``validkit.accents.strip_accents``."""

import pytest

from validkit.accents import strip_accents


def test_strip_accents_removes_french_accents():
    assert strip_accents("Crème brûlée") == "Creme brulee"


def test_strip_accents_removes_umlauts():
    assert strip_accents("äöü") == "aou"


def test_strip_accents_removes_german_umlauts_case_preserved():
    assert strip_accents("ÄÖÜ") == "AOU"


def test_strip_accents_empty_input():
    assert strip_accents("") == ""


def test_strip_accents_text_without_diacritics_is_unchanged():
    assert strip_accents("plain ascii text 123") == "plain ascii text 123"


def test_strip_accents_preserves_non_mark_characters():
    assert strip_accents("café, naïve — déjà vu!") == "cafe, naive — deja vu!"


def test_strip_accents_removes_combining_codepoints_on_precomposed_input():
    assert strip_accents("\u00e9") == "e"


def test_strip_accents_raises_value_error_above_max_length():
    with pytest.raises(ValueError):
        strip_accents("x" * 10001)


def test_strip_accents_at_max_length_is_allowed():
    assert strip_accents("x" * 10000) == "x" * 10000


def test_strip_accents_error_message_does_not_leak_input():
    oversized = "secret-value-" + "x" * 10000
    with pytest.raises(ValueError) as excinfo:
        strip_accents(oversized)
    assert oversized not in str(excinfo.value)
