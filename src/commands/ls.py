"""Команда ls."""
from src.commands.base import Command

class Command(Command):
    """Список содержимого каталога."""

    name = "ls"
    help = "список содержимого каталога"

    def run(self, vfs, args):
        path = args[0] if args else "."
        node = vfs.resolve(path)
        if not node.is_dir:
            return node.name
        return "\n".join(sorted(node.children.keys()))
