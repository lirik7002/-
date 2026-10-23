"""Команда cd."""
from src.commands.base import Command

class Command(Command):
    """Смена текущего каталога."""

    name = "cd"
    help = "переход в каталог"

    def run(self, vfs, args):
        if not args:
            vfs.cwd = vfs.root
            return ""
        node = vfs.resolve(args[0])
        if not node.is_dir:
            raise NotADirectoryError(args[0])
        vfs.cwd = node
        return ""
