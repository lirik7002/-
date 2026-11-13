"""Сбор прямых зависимостей pip-пакета без менеджеров пакетов.

Используется PyPI JSON API и ручной разбор поля requires_dist.
"""
import json
import urllib.request

PYPI_JSON = "https://pypi.org/pypi/{name}/json"
REQUIRES_KEY = "requires_dist"


def fetch_metadata(package, timeout=10):
    """Загружает метаданные пакета с PyPI.

    :param package: имя пакета
    :param timeout: таймаут запроса в секундах
    :return: словарь метаданных
    :raises RuntimeError: при ошибке сети или ответа
    """
    url = PYPI_JSON.format(name=package)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as err:  # noqa: BLE001
        raise RuntimeError(f"Не удалось получить данные: {err}") from err
    return json.loads(raw)


def extract_requires(metadata):
    """Извлекает список requires_dist из метаданных.

    :param metadata: словарь метаданных PyPI
    :return: список строк зависимостей
    """
    info = metadata.get("info", {})
    requires = info.get(REQUIRES_KEY) or []
    return list(requires)


def normalize_dependency(spec):
    """Приводит строку зависимости к имени пакета.

    :param spec: строка вида "requests>=2.0; extra == 'x'"
    :return: имя пакета
    """
    head = spec.split(";", 1)[0].strip()
    for sep in ("==", ">=", "<=", "!=", "~=", ">", "<", "["):
        head = head.split(sep, 1)[0]
    return head.strip()


def collect_direct(package):
    """Возвращает прямые зависимости пакета.

    :param package: имя пакета
    :return: список имён зависимостей
    """
    metadata = fetch_metadata(package)
    specs = extract_requires(metadata)
    result = []
    for spec in specs:
        name = normalize_dependency(spec)
        if name:
            result.append(name)
    return result
