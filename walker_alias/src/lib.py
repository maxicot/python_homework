from typing import Any


class WalkerAlias:
    """Usage example:
    ```python
    from random import random

    walker = WalkerAlias({"A": 0.001, "B": 0.3, "C": (1 - 0.001 - 0.3)}, random)
    print(walker.get_random())
    ```
    """

    def __init__(self, weighted: dict[Any, float], random) -> None:
        """Performs calculations necessary for Walker's alias method.
        Takes a dictionary of items and their weights as floats between 0 and 1,
        as well as a function returning random values between 0 and 1"""

        if sum(weighted.values()) != 1:
            raise Exception("sum of probabilities must be 1")

        self.keys = list(weighted.keys())
        weights = [int(i * 10000) for i in weighted.values()]
        weight_sum = sum(weights)
        length = len(weights)
        probabilities = []
        indices = []
        over = []
        under = []

        for w in weights:
            indices.append(-1)
            probabilities.append(w * length / weight_sum)

        for n, p in enumerate(probabilities):
            if p < 1:
                under.append(n)
            else:
                over.append(n)

        while len(under) > 0 and len(over) > 0:
            i = over[-1]
            j = under.pop()
            probabilities[i] -= 1 - probabilities[i]
            indices[j] = i

            if probabilities[i] < 1:
                under.append(i)
                _ = over.pop()

        self.probabilities = probabilities
        self.indices = indices
        self.random = random
        self.keys = list(weighted.keys())
        self.length = length

    def get_random(self) -> Any:
        random = self.random()
        i = int(random * self.length)

        return (
            self.keys[i]
            if random <= self.probabilities[i]
            else self.keys[self.indices[i]]
        )


if __name__ == "__main__":
    from random import random

    walker = WalkerAlias({"A": 0.001, "B": 0.3, "C": (1 - 0.001 - 0.3)}, random)
    print(walker.get_random())
