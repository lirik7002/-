"""Базовый класс команды."""
from src.vfs import Vfs

class Command:
    """Базовая команда эмулятора."""

    name: str = ""
    help: str = ""

    def run(self, vfs: Vfs, args: list[str]) -> str:
        """Выполняет команду, возвращает текстовый вывод."""
        raise NotImplementedError
