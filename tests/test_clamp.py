"""Tests for validkit.clamp."""

import pytest

from validkit.clamp import clamp


def test_value_within_range_is_unchanged():
    assert clamp(5, 1, 10) == 5


def test_value_below_low_is_raised_to_low():
    assert clamp(0, 1, 10) == 1


def test_value_above_high_is_lowered_to_high():
    assert clamp(20, 1, 10) == 10


def test_value_equal_to_low():
    assert clamp(1, 1, 10) == 1


def test_value_equal_to_high():
    assert clamp(10, 1, 10) == 10


def test_float_values():
    assert clamp(2.5, 1.0, 10.0) == 2.5
    assert clamp(0.0, 1.0, 10.0) == 1.0
    assert clamp(20.0, 1.0, 10.0) == 10.0


def test_float_preserves_float_type():
    assert isinstance(clamp(2.5, 1.0, 10.0), float)


def test_int_preserves_int_type():
    assert isinstance(clamp(5, 1, 10), int)


def test_negative_range():
    assert clamp(-5, -10, -1) == -5
    assert clamp(-20, -10, -1) == -10
    assert clamp(0, -10, -1) == -1


def test_mixed_int_float_boundaries():
    assert clamp(3.5, 1, 10) == 3.5


def test_low_equal_high():
    assert clamp(5, 7, 7) == 7
    assert clamp(9, 7, 7) == 7


def test_low_greater_than_high_raises_valueerror():
    with pytest.raises(ValueError):
        clamp(1, 10, 1)


def test_error_message_does_not_leak_input_values():
    with pytest.raises(ValueError) as excinfo:
        clamp(1, 10, 1)
    message = str(excinfo.value)
    assert "10" not in message
    assert "1" not in message
