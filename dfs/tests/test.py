from src.lib import Graph


def test_basic():
    assert Graph([(1, 2), (2, 3), (3, 1), (3, 4)]).dfs() == [1, 2, 3, 4]
    assert Graph([(5, 2), (2, 3), (3, 1), (3, 4)]).dfs() == [5, 2, 3, 1, 4]
