from functools import reduce
from math import ceil, log


def encode(value: str) -> str:
    code = [0] + [
        int(i) for i in "".join(format(i, "b") for i in bytearray(value, "utf8"))
    ]
    length = len(code) - 1

    r = 1
    while 2**r < length + r + 1:
        r += 1

    for i in range(1, length + r + 1):
        # check if power of 2
        if log(i, 2) == ceil(log(i, 2)):
            code.insert(i, 0)

    for i in range(0, r):
        x = 2**i

        for j in range(1, len(code)):
            if ((j >> i) & 1) == 1 and x != j:
                code[x] = code[x] ^ code[j]

    return "".join(str(i) for i in code)


def decode(value: str) -> tuple[str, int]:
    code = [int(i) for i in value]

    def decoded():
        for i in range(1, len(code)):
            if log(i, 2) != ceil(log(i, 2)):
                yield str(code[i])

    decoded = "".join(decoded())
    position = reduce(lambda x, y: x ^ y, [n for n, bit in enumerate(code) if bit])

    if position == 0:
        position = -1

    return (decoded, position)
