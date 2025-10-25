from hypothesis import given
from hypothesis import strategies as st

from ..src.lib import heapsort


def test_general():
    assert heapsort([0, 8, 3, -1, 5]) == [-1, 0, 3, 5, 8]
    assert heapsort([0, 8, 3, -1, 5], cmp=lambda x, y: x > y) == [8, 5, 3, 0, -1]


def test_special():
    assert heapsort([]) == []
    assert heapsort([1]) == [1]


@given(st.lists(st.integers(), max_size=100))
def test_property(arr):
    assert heapsort(arr) == sorted(arr)


class Custom:
    def __init__(self, n: int):
        self.inner = n

    def __eq__(self, rhs) -> bool:
        return self.inner == rhs.inner

    def into(self) -> int:
        return self.inner


def test_custom():
    assert heapsort([Custom(2), Custom(1)], cmp=lambda x, y: x.inner < y.inner) == [
        Custom(1),
        Custom(2),
    ]
