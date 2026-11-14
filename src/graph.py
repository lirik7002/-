"""Построение графа зависимостей BFS без рекурсии."""
from collections import deque

COLON = ":"
EMPTY = ""


def parse_test_repo(path):
    """Читает тестовый файл описания графа."""
    graph = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or COLON not in line:
                continue
            name, rest = line.split(COLON, 1)
            name = name.strip()
            deps = [d for d in rest.split() if d != EMPTY]
            graph[name] = deps
            for dep in deps:
                graph.setdefault(dep, [])
    return graph


def bfs_collect(graph, root, banned_substring, max_depth):
    """BFS-обход графа без рекурсии."""
    order = []
    edges = []
    visited = {root}
    queue = deque([(root, 0)])
    while queue:
        node, depth = queue.popleft()
        order.append(node)
        if depth >= max_depth:
            continue
        for dep in graph.get(node, []):
            if banned_substring and banned_substring in dep:
                continue
            edges.append((node, dep))
            if dep not in visited:
                visited.add(dep)
                queue.append((dep, depth + 1))
    return order, edges


def bfs_with_collector(root, collector, banned, max_depth):
    """BFS с динамическим сбором зависимостей."""
    order = []
    edges = []
    visited = {root}
    queue = deque([(root, 0)])
    while queue:
        node, depth = queue.popleft()
        order.append(node)
        if depth >= max_depth:
            continue
        try:
            deps = collector(node)
        except RuntimeError:
            deps = []
        for dep in deps:
            if banned and banned in dep:
                continue
            edges.append((node, dep))
            if dep not in visited:
                visited.add(dep)
                queue.append((dep, depth + 1))
    return order, edges
