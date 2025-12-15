from ..src import decode, encode


def test_basic():
    encoded = encode("abc")
    _, error = decode(encoded)

    assert error == -1
