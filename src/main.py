"""CLI-прототип инструмента визуализации зависимостей pip.

Этап 1: разбор и валидация параметров командной строки.
"""
import argparse
import os
import re
import sys

# Константы для устранения магических чисел и строк
MIN_NAME_LEN = 1
MAX_NAME_LEN = 128
PNG_EXT = ".png"
DEFAULT_DEPTH = 3
MAX_DEPTH = 50
URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)
NAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


def parse_args(argv):
    """Разбирает аргументы командной строки.

    :param argv: список аргументов (без имени программы)
    :return: объект argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description="Визуализатор графа зависимостей pip-пакетов",
    )
    parser.add_argument(
        "--package", required=True, help="Имя анализируемого пакета",
    )
    parser.add_argument(
        "--repo", required=True,
        help="URL репозитория или путь к тестовому файлу",
    )
    parser.add_argument(
        "--test-mode", action="store_true",
        help="Режим работы с тестовым репозиторием",
    )
    parser.add_argument(
        "--output", default="graph.png",
        help="Имя файла изображения графа",
    )
    parser.add_argument(
        "--filter", default="",
        help="Подстрока для фильтрации пакетов",
    )
    return parser.parse_args(argv)


def validate_package(name):
    """Проверяет имя пакета.

    :param name: имя пакета
    :raises ValueError: если имя некорректно
    """
    if not isinstance(name, str):
        raise ValueError("Имя пакета должно быть строкой")
    if not (MIN_NAME_LEN <= len(name) <= MAX_NAME_LEN):
        raise ValueError("Недопустимая длина имени пакета")
    if not NAME_PATTERN.match(name):
        raise ValueError(
            "Имя пакета содержит недопустимые символы",
        )


def validate_repo(repo, test_mode):
    """Проверяет URL репозитория или путь к тестовому файлу.

    :param repo: URL или путь
    :param test_mode: флаг тестового режима
    :raises ValueError: если параметр некорректен
    """
    if test_mode:
        if not os.path.isfile(repo):
            raise ValueError("Тестовый файл не найден: " + repo)
        return
    if not URL_PATTERN.match(repo):
        raise ValueError("URL должен начинаться с http(s)://")


def validate_output(filename):
    """Проверяет имя выходного файла.

    :param filename: имя файла
    :raises ValueError: если расширение не .png
    """
    if not filename.lower().endswith(PNG_EXT):
        raise ValueError("Файл графа должен иметь расширение .png")
    parent = os.path.dirname(filename) or "."
    if not os.path.isdir(parent):
        raise ValueError("Каталог для файла не существует")


def validate_filter(substring):
    """Проверяет подстроку фильтрации.

    :param substring: подстрока
    :raises ValueError: если подстрока содержит запрещённые символы
    """
    if substring and not NAME_PATTERN.match(substring):
        raise ValueError("Подстрока фильтра содержит недопустимые символы")


def print_params(args):
    """Выводит параметры в формате ключ-значение.

    :param args: разобранные аргументы
    """
    pairs = [
        ("package", args.package),
        ("repo", args.repo),
        ("test-mode", str(args.test_mode)),
        ("output", args.output),
        ("filter", args.filter),
    ]
    for key, value in pairs:
        print(f"{key} = {value}")


def main(argv=None):
    """Точка входа приложения.

    :param argv: аргументы командной строки
    :return: код возврата
    """
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)
    try:
        validate_package(args.package)
        validate_repo(args.repo, args.test_mode)
        validate_output(args.output)
        validate_filter(args.filter)
    except ValueError as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        return 1
    print_params(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
