"""Топологический порядок загрузки для графа зависимостей."""

from collections import defaultdict, deque

from src.constants import ORDER_WIDTH


def load_order(graph: dict[str, list[str]]) -> list[str]:
    """Вернуть порядок загрузки: зависимости раньше зависимых.

    Реализация — алгоритм Кана. Узлы, входящие в циклы, добавляются
    в конец в алфавитном порядке.

    Аргументы:
        graph: словарь «узел -> список зависимостей».

    Возвращает:
        Список имён в порядке загрузки.
    """
    indegree: dict[str, int] = {node: 0 for node in graph}
    reverse: dict[str, list[str]] = defaultdict(list)

    for node, deps in graph.items():
        for dep in deps:
            if dep in indegree:
                indegree[dep] += 1
                reverse[dep].append(node)

    sources = sorted(
        node for node, value in indegree.items() if value == 0
    )
    queue: deque[str] = deque(sources)
    order: list[str] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for nxt in reverse[current]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    cyclic = sorted(node for node in graph if node not in order)
    order.extend(cyclic)
    return order


def cyclic_nodes(graph: dict[str, list[str]]) -> list[str]:
    """Вернуть узлы, входящие в циклы.

    Аргументы:
        graph: граф зависимостей.

    Возвращает:
        Список имён узлов-участников циклов.
    """
    ordered = set(load_order(graph))
    return [node for node in graph if node not in ordered]


def format_order(order: list[str]) -> str:
    """Отформатировать порядок загрузки в виде нумерованного списка.

    Аргументы:
        order: список имён.

    Возвращает:
        Строку для печати.
    """
    return "\n".join(
        f"{index:>{ORDER_WIDTH}}. {name}"
        for index, name in enumerate(order, 1)
    )
