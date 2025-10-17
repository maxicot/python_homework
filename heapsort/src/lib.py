from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


# Recursive heapsort implementation.
# The default behavior of `cmp` is to check
# whether the first argument is smaller than the second.
# A custom `cmp` is mandatory in case `T` doesn't support comparisons
def heapsort(array: list, cmp: Callable[[T, T], bool] = lambda x, y: x < y) -> list:
    n = len(array)

    if n < 2:
        return array

    def heapify(array: list, n: int, i: int) -> list:
        left = 2 * i + 1
        right = left + 1
        largest = i

        if left < n and cmp(array[largest], array[left]):
            largest = left

        if right < n and cmp(array[largest], array[right]):
            largest = right

        if largest != i:
            (array[i], array[largest]) = (array[largest], array[i])
            return heapify(array, n, largest)

        return array

    for i in range(n // 2, -1, -1):
        array = heapify(array, n, i)

    for i in range(n - 1, 0, -1):
        (array[i], array[0]) = (array[0], array[i])
        array = heapify(array, i, 0)

    return array
