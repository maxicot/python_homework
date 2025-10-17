from itertools import permutations


# Переборное решение
def bruteforce(n: int) -> int:
    def is_valid(permutation: list, n: int) -> int:
        for i in range(n):
            for j in range(i + 1, n):
                # Диагональные конфликты
                if abs(permutation[i] - permutation[j]) == abs(i - j):
                    return 0
        return 1

    result = 0
    # Проверка перестановок номеров колонок
    for permutation in permutations(range(n)):
        result += is_valid(permutation, n)

    return result


# Рекурсивное решение
def recursive(n: int) -> int:
    def is_valid(positions: list, row: int, column: int) -> bool:
        for r in range(row):
            c = positions[r]
            # Проверка колонок и диагоналей
            if c == column or abs(c - column) == abs(r - row):
                return False
        return True

    def backtrack(positions: list, row: int, n: int) -> int:
        if row == n:  # Валидное решение
            return 1

        result = 0
        for column in range(n):
            if is_valid(positions, row, column):
                positions[row] = column
                result += backtrack(positions, row + 1, n)
        return result

    return backtrack([-1] * n, 0, n)


# Итеративное решение через битовые маски
def bitmasks(n: int) -> int:
    stack = [(0, 0, 0, 0)]
    result = 0

    while len(stack) > 0:
        row, cols, diag1, diag2 = stack.pop()

        if row == n:
            # Валидное решение
            result += 1
            continue

        for col in range(n):
            # Безопасна ли позиция
            col_mask = 1 << col
            diag1_mask = 1 << (row - col + n - 1)
            diag2_mask = 1 << (row + col)
            if (
                (cols & col_mask) == 0
                and (diag1 & diag1_mask) == 0
                and (diag2 & diag2_mask) == 0
            ):
                # Ставим нового ферзя
                new_cols = cols | col_mask
                new_diag1 = diag1 | diag1_mask
                new_diag2 = diag2 | diag2_mask
                stack.append((row + 1, new_cols, new_diag1, new_diag2))

    return result
