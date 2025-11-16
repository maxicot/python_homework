from itertools import batched


class TreeNode:
    def __init__(self, value: str):
        self.left: None | TreeNode = None
        self.right: None | TreeNode = None
        self.value = value


def sorted_insert(lst: list, value, key):
    target_idx = 0
    for i in range(len(lst)):
        target_idx = i
        if key(lst[i]) > key(value):
            break
    lst.insert(target_idx, value)


# Huffman's coding
def encode(inp: str) -> tuple[str, dict[str, str]]:
    # edded end case checks
    if len(inp) == 0:
        return ("", {})

    if len(inp) == 1:
        return ("0", {"0": inp[0]})

    output_string = ""
    dictionary = {}

    frequencies = {}
    for chr in inp:
        if chr in frequencies:
            frequencies[chr] += 1
        else:
            frequencies[chr] = 1
    srt = sorted(frequencies.items(), key=lambda x: x[1])
    nodes = [(TreeNode(char), value) for (char, value) in srt]

    while len(nodes) > 1:
        s1, s2 = nodes.pop(0), nodes.pop(0)
        node = TreeNode(s1[0].value + s2[0].value)
        node.left = s1[0]
        node.right = s2[0]
        sorted_insert(
            nodes,
            (node, s1[1] + s2[1]),
            lambda x: x[1],
        )

    root = nodes[0][0]

    def walk(node, acc):
        if node.left is None and node.right is None:
            dictionary[node.value] = acc
        else:
            if node.left is not None:
                walk(node.left, acc + "0")
            if node.right is not None:
                walk(node.right, acc + "1")

    walk(root, "")

    for ch in inp:
        output_string += dictionary[ch]

    # modified the original code to provide a more convenient dict
    return (output_string, {v: k for k, v in dictionary.items()})


# new code


# Decode a string encoded with `encode`
def decode(encoded: str, table: dict[str, str]) -> str:
    if len(table) == 0:
        return ""

    max_len = max(map(len, table.keys()))
    res = ""

    def retrieve() -> str | None:
        nonlocal encoded

        for length in range(1, max_len + 1):
            symbol = table.get(encoded[0:length])

            if symbol:
                encoded = encoded[length:]
                return symbol

        return None

    while encoded:
        symbol = retrieve()

        if not symbol:
            raise Exception("invalid sequence")

        res += symbol

    return res


def bytify(s: str) -> str:
    return "".join(chr(int("".join(i), 2)) for i in batched(s, 8))


def encode_bytes(inp: str) -> tuple[str, dict[str, str], int]:
    encoded, table = encode(inp)
    padding = 8 - len(encoded) % 8

    if padding == 8:
        padding = 0

    aligned = "0" * padding + encoded

    return (bytify(aligned), table, padding)


def decode_bytes(encoded: str, table: dict[str, str], padding: int) -> str:
    encoded = "".join(format(ord(i), "08b") for i in encoded)[padding:]
    return decode(encoded, table)


# Produce a standalone file format for a given input.
#
# Usage example:
# ```
# with open('file', newline = '') as f, open('file_encoded', 'w') as e:
#     e.write(encode_file(f.read()))
# ```
def encode_file(inp: str) -> str:
    encoded, table, padding = encode_bytes(inp)
    global dump_a
    dump_a = table

    # File format:
    # padding size (1 byte) + table length (1 byte)
    # + table {code size (1 byte) + code (1 to 32 bytes) + byte} (up to 256 times)
    # + padding bits + encoded contents

    def process_entry(entry: tuple[str, str]) -> str:
        key, value = entry
        size = len(key)
        pad = 8 - size % 8
        code = bytify("0" * (pad if pad != 8 else 0) + key)

        return chr(size) + code + value

    length = chr(len(table))
    table = "".join(map(process_entry, table.items()))

    return chr(padding) + length + table + encoded


# Decode a file encoded with `encode_file`.
# IMPORTANT: specify `open`'s `newline` argument to be an empty string.
#
# Usage example:
# ```
# with open('file', newline = '') as f, open('file_decoded', 'w', newline = '') as d:
#     d.write(decode_file(f.read()))
# ```
def decode_file(encoded: str) -> str:
    padding = ord(encoded[0])
    length = ord(encoded[1])
    encoded = encoded[2:]

    def mul_of_8(i: int) -> int:
        rem = i % 8
        return i - rem + (0 if rem == 0 else 8)

    table = {}

    while length > 0:
        size = ord(encoded[0])
        bits = mul_of_8(size)
        code = encoded[1 : 1 + bits // 8]
        code = "".join(format(ord(i), "08b") for i in code)[-size:]
        encoded = encoded[1 + bits // 8 :]
        value = encoded[0]
        encoded = encoded[1:]
        table[code] = value
        length -= 1

    return decode_bytes(encoded, table, padding)
