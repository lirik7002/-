"""Команда exit."""
from src.commands.base import Command

class Command(Command):
    """Выход из эмулятора."""

    name = "exit"
    help = "выход из эмулятора"

    def run(self, vfs, args):
        raise SystemExit(0)
