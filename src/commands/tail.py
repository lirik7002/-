"""Команда tail."""
from src.commands.base import Command

DEFAULT_LINES = 10

class Command(Command):
    """Последние n строк файла."""

    name = "tail"
    help = "последние n строк файла"

    def run(self, vfs, args):
        if not args:
            raise ValueError("usage: tail <file> [n]")
        node = vfs.resolve(args[0])
        if node.is_dir:
            raise IsADirectoryError(args[0])
        n = int(args[1]) if len(args) > 1 else DEFAULT_LINES
        lines = node.content.decode("utf-8", errors="replace").splitlines()
        return "\n".join(lines[-n:])
