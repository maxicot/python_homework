# Extended Euclidean algorithm
def gcd(a: int, b: int) -> int:
    while b != 0:
        (a, b) = (b, a - (a // b) * b)

    return a
