"""Команда tree."""
from src.commands.base import Command

INDENT = "    "

class Command(Command):
    """Рекурсивное дерево каталогов."""

    name = "tree"
    help = "рекурсивное дерево каталогов"

    def run(self, vfs, args):
        path = args[0] if args else "."
        node = vfs.resolve(path)
        if not node.is_dir:
            return node.name
        lines: list[str] = [node.name]

        def walk(cur, prefix):
            items = sorted(cur.children.values(), key=lambda n: n.name)
            for i, child in enumerate(items):
                last = i == len(items) - 1
                branch = "└── " if last else "├── "
                lines.append(prefix + branch + child.name)
                if child.is_dir:
                    walk(child, prefix + ("    " if last else "│   "))

        walk(node, "")
        return "\n".join(lines)
