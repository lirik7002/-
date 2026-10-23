"""Парсер командной строки с поддержкой кавычек."""
import shlex

class ParseError(Exception):
    """Ошибка разбора строки."""

def parse_command(line: str) -> tuple[str, list[str]]:
    """Разбирает строку на команду и аргументы.

    Поддерживает одинарные и двойные кавычки, экранирование.
    """
    try:
        tokens = shlex.split(line, posix=True)
    except ValueError as exc:
        raise ParseError(f"Ошибка разбора: {exc}") from exc
    if not tokens:
        return "", []
    return tokens[0], tokens[1:]
