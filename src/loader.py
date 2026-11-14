"""Определение порядка загрузки зависимостей (топологический порядок)."""
from collections import deque


def topological_order(graph, root):
    """Топологическая сортировка подграфа, достижимого из root."""
    reachable = _reachable_nodes(graph, root)
    in_degree = {node: 0 for node in reachable}
    for node in reachable:
        for dep in graph.get(node, []):
            if dep in in_degree:
                in_degree[dep] += 1
    queue = deque(
        n for n in reachable if in_degree[n] == 0 and n != root
    )
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for parent in reachable:
            if node in graph.get(parent, []):
                in_degree[parent] -= 1
                if in_degree[parent] == 0 and parent != root:
                    queue.append(parent)
    return order


def _reachable_nodes(graph, root):
    """Множество узлов, достижимых из root."""
    seen = set()
    stack = [root]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.get(node, []))
    return seen
