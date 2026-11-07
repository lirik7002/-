"""Визуализация графа зависимостей в D2 и PNG."""

import os
import shutil
import subprocess
import tempfile

from src.constants import D2_SUFFIX, DEFAULT_ENCODING, LAYOUT_FILE


def to_d2(graph: dict[str, list[str]]) -> str:
    """Сформировать текст диаграммы на языке D2.

    Аргументы:
        graph: граф зависимостей.

    Возвращает:
        Строку с исходником D2.
    """
    lines: list[str] = []
    for node, deps in graph.items():
        if not deps:
            lines.append(f'"{node}"')
            continue
        lines.extend(f'"{node}" -> "{dep}"' for dep in deps)
    return "\n".join(lines)


def _resolve_d2() -> str:
    """Найти исполняемый файл d2 в PATH.

    Возвращает:
        Путь к бинарнику d2.

    Исключения:
        RuntimeError: если d2 не установлен.
    """
    path = shutil.which("d2")
    if path is None:
        raise RuntimeError(
            "d2 не найден, инструкция: https://d2lang.com/tour/install"
        )
    return path


def render_png(graph: dict[str, list[str]], out_png: str) -> str:
    """Сохранить D2 рядом с PNG и отрендерить изображение.

    Аргументы:
        graph: граф зависимостей.
        out_png: путь к выходному PNG.

    Возвращает:
        Путь к сохранённому .d2-файлу.

    Исключения:
        RuntimeError: если d2 недоступен.
    """
    d2_binary = _resolve_d2()
    out_png = os.path.abspath(out_png)
    d2_path = os.path.splitext(out_png)[0] + D2_SUFFIX

    with open(d2_path, "w", encoding=DEFAULT_ENCODING) as handle:
        handle.write(to_d2(graph))

    with tempfile.TemporaryDirectory() as tmp:
        layout_path = os.path.join(tmp, LAYOUT_FILE)
        subprocess.run(
            [d2_binary, d2_path, layout_path],
            check=True,
        )
        subprocess.run(
            [d2_binary, layout_path, out_png],
            check=True,
        )
    return d2_path
