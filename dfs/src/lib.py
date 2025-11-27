class Graph[T]:
    def __init__(self, edges: list[tuple[T, T]]):
        # Check, but not use a set as we want ordering
        if len(set(edges)) != len(edges):
            raise Exception("two same edges")

        # {vertex: adjacent_vertices}
        self.__vertices: dict[T, list[T]] = {}

        for edge in edges:
            if edge[0] == edge[1]:
                raise Exception("vertex linked with itself")

            self.__vertices.setdefault(edge[0], []).append(edge[1])
            self.__vertices.setdefault(edge[1], []).append(edge[0])

    # Returns vertices in the order they're visited during dfs
    def dfs(self) -> list[T]:
        # Writing Python anyway already, so why not
        status = {
            "not visited": self.__vertices.copy(),
            "to be visited": [],
            "visited": [],
        }

        while len(status["not visited"]) != 0:
            if len(status["to be visited"]) == 0:
                status["to be visited"].append(
                    status["not visited"].__iter__().__next__()
                )

            while len(status["to be visited"]) != 0:
                vertex = status["to be visited"][0]
                status["to be visited"].remove(vertex)

                if vertex in status["not visited"]:
                    del status["not visited"][vertex]
                    status["to be visited"].extend(self.__vertices[vertex])
                    status["visited"].append(vertex)

        return status["visited"]


gr = Graph([(1, 2), (2, 3), (3, 1), (3, 4)])
print(gr.dfs())
