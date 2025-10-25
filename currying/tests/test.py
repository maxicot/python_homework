from ..src.lib import curry
import pytest


def add_args(*args):
    return sum(args)


def add2(a, b):
    return a + b


def test_specified():
    assert curry(add_args, 3)(1)(2)(3) == 6


def test_negative():
    with pytest.raises(Exception) as e:
        curry(add2, -1)
        assert e == "negative arity"


def test_less():
    with pytest.raises(Exception) as e:
        curry(add2, 1)
        assert e == "specified arity is lesser than required"


def test_unspecified():
    assert curry(add2)(1)(2) == 3


def test_zero():
    assert curry(add_args, 0)() == 0
