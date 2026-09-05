"""Tests for :func:`validkit.slug.slugify`."""

import pytest

from validkit.slug import slugify


def test_slugify_lowercases_and_strips_accents():
    assert slugify("Héllo Wörld!") == "hello-world"


def test_slugify_preserves_existing_word_characters():
    assert slugify("Hello World") == "hello-world"
    assert slugify("foo_bar") == "foo_bar"


def test_slugify_empty_string_returns_empty():
    assert slugify("") == ""


def test_slugify_only_special_characters_returns_empty():
    assert slugify("!!!") == ""
    assert slugify("...") == ""
    assert slugify("--") == ""


def test_slugify_collapses_repeated_separators():
    assert slugify("a---b") == "a-b"
    assert slugify("a   b") == "a-b"


def test_slugify_trims_leading_and_trailing_separators():
    assert slugify("-hello-world-") == "hello-world"
    assert slugify("  hello world  ") == "hello-world"


def test_slugify_handles_mixed_diacritics_and_punctuation():
    assert slugify("Crème brûlée") == "creme-brulee"


def test_slugify_raises_above_max_length():
    with pytest.raises(ValueError):
        slugify("x" * 10001)


def test_slugify_allows_at_or_below_max_length():
    assert slugify("a" * 10000) == "a" * 10000


def test_slugify_error_message_does_not_leak_input():
    secret = "x" * 10001
    with pytest.raises(ValueError) as excinfo:
        slugify(secret)
    assert secret not in str(excinfo.value)
