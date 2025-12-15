from random import random

import pytest

from ..src import WalkerAlias


def test_edge():
    walker = WalkerAlias({"A": 0, "B": 0.3, "C": 0.7}, random)

    for _ in range(100):
        assert walker.get_random() != "A"


def test_validity():
    with pytest.raises(Exception) as e:
        # 0.1 + 0.5 + 0.5 > 1
        walker = WalkerAlias({"A": 0.1, "B": 0.5, "C": 0.5}, random)
        walker.get_random()

        assert e == "sum of probabilities must be 1"


def test_values():
    keys = ["A", "B", "C"]
    weights = [0.1, 0.3, 0.6]
    walker = WalkerAlias(dict(zip(keys, weights)), random)

    for _ in range(100):
        assert walker.get_random() in keys
