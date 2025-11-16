from hypothesis import given
from hypothesis import strategies as st
from src import decode_file, encode_file


@given(st.text())
def test_property(file: str):
    assert decode_file(encode_file(file)) == file
