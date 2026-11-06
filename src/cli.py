"""Интерфейс командной строки: разбор аргументов и валидация."""

import argparse
import os
import re
import sys
from urllib.parse import urlparse

from src.config import Config
from src.constants import EXIT_INVALID_ARGS, PNG_SUFFIX

PACKAGE_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def build_parser() -> argparse.ArgumentParser:
    """Создать парсер аргументов со всеми опциями инструмента.

    Возвращает:
        Настроенный argparse.ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="depviz",
        description="Визуализация графа зависимостей пакета pip.",
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Имя анализируемого пакета",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="URL PyPI либо путь к файлу тестового графа",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["online", "test"],
        help="Режим: online (PyPI) или test (локальный файл)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Имя выходного PNG-файла",
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Подстрока; пакеты с ней исключаются",
    )
    return parser


def _validate_package(name: str) -> list[str]:
    """Проверить имя пакета.

    Аргументы:
        name: имя пакета.

    Возвращает:
        Список строк с описанием ошибок (пустой, если всё корректно).
    """
    if not name or not PACKAGE_RE.match(name):
        return ["package: ожидаются буквы, цифры, '.', '_', '-'"]
    return []


def _validate_online_repo(repo: str) -> list[str]:
    """Проверить URL репозитория для онлайн-режима.

    Аргументы:
        repo: строка URL.

    Возвращает:
        Список ошибок (пустой при корректном URL).
    """
    parsed = urlparse(repo)
    valid = parsed.scheme in ("http", "https") and bool(parsed.netloc)
    if not valid:
        return ["repo: в онлайн-режиме ожидается http(s)-URL"]
    return []


def _validate_repo(repo: str, mode: str) -> list[str]:
    """Проверить аргумент репозитория с учётом режима.

    Аргументы:
        repo: URL или путь к файлу.
        mode: "online" или "test".

    Возвращает:
        Список ошибок.
    """
    if mode == "online":
        return _validate_online_repo(repo)
    if not os.path.isfile(repo):
        return [f"repo: тестовый файл не найден: {repo}"]
    return []


def _validate_output(path: str) -> list[str]:
    """Проверить имя выходного PNG-файла и его директорию.

    Аргументы:
        path: имя файла.

    Возвращает:
        Список ошибок.
    """
    errors: list[str] = []
    if not path.lower().endswith(PNG_SUFFIX):
        errors.append("output: имя файла должно оканчиваться на .png")
    out_dir = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(out_dir):
        errors.append(f"output: директория не существует: {out_dir}")
    return errors


def validate(args: argparse.Namespace) -> list[str]:
    """Полная валидация всех параметров.

    Аргументы:
        args: разобранные аргументы argparse.

    Возвращает:
        Список человекочитаемых ошибок.
    """
    errors: list[str] = []
    errors += _validate_package(args.package)
    errors += _validate_repo(args.repo, args.mode)
    errors += _validate_output(args.output)
    return errors


def parse_args(argv: list[str] | None = None) -> Config:
    """Разобрать argv и завершить процесс при ошибке валидации.

    Аргументы:
        argv: список аргументов; None — взять sys.argv.

    Возвращает:
        Заполненный объект Config.

    Исключения:
        SystemExit: с кодом EXIT_INVALID_ARGS при невалидных данных.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    errors = validate(args)
    if errors:
        for error in errors:
            print(f"[ОШИБКА] {error}", file=sys.stderr)
        sys.exit(EXIT_INVALID_ARGS)
    return Config(
        package=args.package,
        repo=args.repo,
        mode=args.mode,
        output=args.output,
        exclude=args.exclude,
    )


def print_config(cfg: Config) -> None:
    """Вывести все параметры пользователя в формате ключ-значение.

    Аргументы:
        cfg: конфигурация для вывода.
    """
    print(f"package = {cfg.package}")
    print(f"repo    = {cfg.repo}")
    print(f"mode    = {cfg.mode}")
    print(f"output  = {cfg.output}")
    print(f"exclude = {cfg.exclude!r}")
