"""Команда touch."""
from src.commands.base import Command
from src.vfs import VfsNode

class Command(Command):
    """Создание пустого файла (в памяти)."""

    name = "touch"
    help = "создать пустой файл (только в памяти)"

    def run(self, vfs, args):
        if not args:
            raise ValueError("usage: touch <path>")
        path = args[0]
        parent_path, _, name = path.rpartition("/")
        parent = vfs.resolve(parent_path) if parent_path else vfs.cwd
        if name in parent.children:
            return ""
        node = VfsNode(name=name, is_dir=False, parent=parent)
        parent.children[name] = node
        return ""
