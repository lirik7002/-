"""Конфигурация инструмента, общая для CLI и пайплайна."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Параметры, заданные пользователем через командную строку.

    Атрибуты:
        package: имя анализируемого пакета.
        repo: URL репозитория PyPI либо путь к файлу тестового графа.
        mode: режим работы — "online" (PyPI) или "test" (локальный файл).
        output: имя выходного PNG-файла.
        exclude: подстрока; пакеты, содержащие её, исключаются.
    """

    package: str
    repo: str
    mode: str
    output: str
    exclude: str = ""
