"""REPL-движок: регистрация и выполнение команд."""
from src.parser import parse_command
from src.commands.base import Command

class UnknownCommandError(Exception):
    """Неизвестная команда."""

class Shell:
    """Оболочка с набором команд."""

    def __init__(self, vfs, output_callback):
        self.vfs = vfs
        self._out = output_callback
        self._commands: dict[str, Command] = {}
        self._register_commands()

    def _register_commands(self) -> None:
        from src.commands import ls, cd, tail, tree, mkdir, touch, exit_cmd
        for module in (ls, cd, tail, tree, mkdir, touch, exit_cmd):
            cmd = module.Command()
            self._commands[cmd.name] = cmd

    def echo(self, text: str) -> None:
        """Выводит текст через callback."""
        self._out(text)

    def execute(self, line: str) -> str:
        """Выполняет строку, возвращает вывод."""
        name, args = parse_command(line)
        if not name:
            return ""
        if name == "exit":
            raise SystemExit(0)
        cmd = self._commands.get(name)
        if cmd is None:
            raise UnknownCommandError(f"команда не найдена: {name}")
        return cmd.run(self.vfs, args)
