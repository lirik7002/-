"""Тесты валидации параметров этапа 1."""
import pytest

from src import main


def test_validate_package_ok():
    """Корректное имя пакета проходит проверку."""
    main.validate_package("requests")


def test_validate_package_empty():
    """Пустое имя пакета отклоняется."""
    with pytest.raises(ValueError):
        main.validate_package("")


def test_validate_package_bad_chars():
    """Недопустимые символы отклоняются."""
    with pytest.raises(ValueError):
        main.validate_package("re quests")


def test_validate_repo_url():
    """Корректный URL проходит проверку."""
    main.validate_repo("https://pypi.org", False)


def test_validate_repo_bad_url():
    """Некорректный URL отклоняется."""
    with pytest.raises(ValueError):
        main.validate_repo("ftp://pypi.org", False)


def test_validate_output_ok():
    """Файл с .png проходит проверку."""
    main.validate_output("graph.png")


def test_validate_output_bad_ext():
    """Файл без .png отклоняется."""
    with pytest.raises(ValueError):
        main.validate_output("graph.jpg")


def test_validate_filter_ok():
    """Корректная подстрока проходит проверку."""
    main.validate_filter("test")


def test_validate_filter_bad():
    """Некорректная подстрока отклоняется."""
    with pytest.raises(ValueError):
        main.validate_filter("bad filter")
