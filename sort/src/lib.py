from typing import TypeVar
from collections.abc import Callable

T = TypeVar('T')

# An all too recursive implementation of merge sort.
# Either comparisons between elements must be supported
# on the type's level or the `cmp` argument must be provided.
# The default behavior of `cmp` is to check
# whether the first argument is lesser than the second
def merge_sort(array: list, cmp: Callable[[T, T], bool] = lambda x, y: x < y) -> list:
    if len(array) < 2:
        return array

    middle = len(array) // 2
    left = merge_sort(array[middle:], cmp)
    right = merge_sort(array[:middle], cmp)

    return merge(left, right, cmp)

def merge(left: list, right: list, cmp: Callable[[T, T], bool]) -> list:
    if not left:
        return right
    if not right:
        return left

    left, right = (left, right) if cmp(left[0], right[0]) else (right, left)

    return [left[0]] + merge(left[1:], right, cmp)
