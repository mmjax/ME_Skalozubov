import pytest


def test_add(calc):
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(-1, -1) == -2


def test_subtract(calc):
    assert calc.subtract(10, 5) == 5
    assert calc.subtract(-1, -1) == 0
    assert calc.subtract(-1, 1) == -2


def test_multiply(calc):
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(-1, 1) == -1
    assert calc.multiply(0, 10) == 0


def test_divide(calc):
    assert calc.divide(10, 2) == 5
    assert calc.divide(-4, 2) == -2
    assert calc.divide(5, 2) == 2.5


def test_divide_by_zero(calc):
    with pytest.raises(ValueError) as exc_info:
        calc.divide(10, 0)
    assert str(exc_info.value) == "Cannot divide by zero"