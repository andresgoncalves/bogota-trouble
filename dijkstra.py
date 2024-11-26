import sys
from typing import Callable


# Distancia, Predecesor, Visitado
type DijkstraTable = list[tuple[int, int, bool]]

M = sys.maxsize


def dijkstra(start: int, matrix: list[list[int]], callback: Callable[[int, int], None] = lambda x, y: None,
             handicap: int = 0):
    table = [
        (0 if node == start else M, -1, False) for node in range(len(matrix))
    ]

    return _dijkstra(start, matrix, table, callback, handicap)


def get_dijkstra_distance(table: DijkstraTable, end: int):
    return table[end][0]


def get_dijkstra_route(table: DijkstraTable, end: int):
    route = [end]
    node = end
    while table[node][1] >= 0:
        next = table[node][1]
        route.insert(0, next)
        node = next
    return route


def _dijkstra(
    current: int | None,
    matrix: list[list[int]],
    table: DijkstraTable,
    callback: Callable[[int, int], None],
    handicap: int
) -> DijkstraTable:
    if current == None:
        return table

    for node, distance in enumerate(matrix[current]):
        total_distance = table[current][0] + distance
        if distance > 0:
            total_distance += handicap
        if total_distance < table[node][0]:
            table[node] = (total_distance, current, table[node][2])

    table[current] = (table[current][0], table[current][1], True)

    next = None
    min_distance = 0
    for node, total_distance in enumerate(table):
        if not table[node][2] and (next == None or total_distance < min_distance):
            next, min_distance = node, total_distance

    callback(current, next)

    return _dijkstra(next, matrix, table, callback, handicap)
