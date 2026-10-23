"""Команда mkdir."""
from src.commands.base import Command
from src.vfs import VfsNode

class Command(Command):
    """Создание каталога (в памяти)."""

    name = "mkdir"
    help = "создать каталог (только в памяти)"

    def run(self, vfs, args):
        if not args:
            raise ValueError("usage: mkdir <path>")
        path = args[0]
        node = VfsNode(name="", is_dir=True)
        vfs.add(path, node)
        return ""
