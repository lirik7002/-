"""Построение графа зависимостей нерекурсивным BFS."""

from collections import deque
from typing import Callable

from src.constants import COMMENT_PREFIX, NODE_SEPARATOR

GetDeps = Callable[[str], list[str]]


def load_test_graph(path: str) -> dict[str, list[str]]:
    """Разобрать тестовый файл графа вида ``A: B C``.

    Аргументы:
        path: путь к файлу.

    Возвращает:
        Словарь «узел -> список зависимостей».
    """
    graph: dict[str, list[str]] = {}
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith(COMMENT_PREFIX):
                continue
            node, _, deps = line.partition(NODE_SEPARATOR)
            graph[node.strip()] = deps.split()
    return graph


def bfs_graph(
    start: str,
    get_deps: GetDeps,
    exclude: str = "",
) -> dict[str, list[str]]:
    """Обойти граф в ширину без рекурсии.

    Аргументы:
        start: стартовый узел.
        get_deps: функция «узел -> список зависимостей».
        exclude: подстрока; узлы с ней не раскрываются и не добавляются.

    Возвращает:
        Словарь достижимых узлов с их зависимостями.

    Примечания:
        Циклы обрабатываются множеством ``seen``.
    """
    seen = {start}
    graph: dict[str, list[str]] = {}
    queue: deque[str] = deque([start])

    while queue:
        node = queue.popleft()
        deps = [dep for dep in get_deps(node) if exclude not in dep]
        graph[node] = deps
        for dep in deps:
            if dep not in seen:
                seen.add(dep)
                queue.append(dep)
    return graph


def _make_pypi_getter(repo_url: str) -> GetDeps:
    """Создать кэширующий getter для режима PyPI.

    Аргументы:
        repo_url: базовый URL репозитория.

    Возвращает:
        Функцию «имя -> список прямых зависимостей».
    """
    from src.fetcher import fetch_direct_dependencies
    cache: dict[str, list[str]] = {}

    def getter(name: str) -> list[str]:
        if name not in cache:
            try:
                cache[name] = fetch_direct_dependencies(name, repo_url)
            except RuntimeError:
                cache[name] = []
        return cache[name]

    return getter


def build_from_pypi(
    package: str,
    repo_url: str,
    exclude: str = "",
) -> dict[str, list[str]]:
    """Построить граф зависимостей для реального пакета PyPI.

    Аргументы:
        package: имя пакета.
        repo_url: базовый URL репозитория.
        exclude: подстрока для фильтрации.

    Возвращает:
        Граф зависимостей.
    """
    return bfs_graph(
        package.lower(),
        _make_pypi_getter(repo_url),
        exclude=exclude,
    )


def _make_test_getter(path: str) -> GetDeps:
    """Создать getter на основе локального файла.

    Аргументы:
        path: путь к тестовому файлу.

    Возвращает:
        Функцию «имя -> список зависимостей».
    """
    source = load_test_graph(path)

    def getter(name: str) -> list[str]:
        return source.get(name, [])

    return getter


def build_from_test(
    start: str,
    path: str,
    exclude: str = "",
) -> dict[str, list[str]]:
    """Построить граф из локального файла описания.

    Аргументы:
        start: стартовый узел.
        path: путь к файлу.
        exclude: подстрока для фильтрации.

    Возвращает:
        Граф зависимостей.
    """
    return bfs_graph(start, _make_test_getter(path), exclude=exclude)
