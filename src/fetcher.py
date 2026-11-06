"""Получение прямых зависимостей пакета pip с PyPI."""

import io
import json
import re
import tarfile
import urllib.request
import zipfile

from src.constants import (
    DECODE_ERRORS,
    DEFAULT_ENCODING,
    EXTRA_MARKER,
    HTTP_TIMEOUT_LONG_SEC,
    HTTP_TIMEOUT_SHORT_SEC,
    METADATA_SUFFIX,
    REQUIRES_DIST_PREFIX,
    SDIST_SUFFIX,
)

_SPEC_RE = re.compile(r"^\s*([A-Za-z0-9._-]+)")


def _download(url: str, timeout: int) -> bytes:
    """Скачать url и вернуть байты.

    Аргументы:
        url: адрес ресурса.
        timeout: таймаут в секундах.

    Возвращает:
        Тело ответа в виде bytes.
    """
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


def _read_wheel_metadata(raw: bytes) -> str:
    """Извлечь текст METADATA из wheel-архива.

    Аргументы:
        raw: содержимое wheel-файла в байтах.

    Возвращает:
        Текст файла METADATA.
    """
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        name = next(
            item for item in archive.namelist()
            if item.endswith(METADATA_SUFFIX)
        )
        payload = archive.read(name)
    return payload.decode(DEFAULT_ENCODING, DECODE_ERRORS)


def _read_sdist_metadata(raw: bytes) -> str:
    """Извлечь текст PKG-INFO из sdist-архива.

    Аргументы:
        raw: содержимое tar.gz в байтах.

    Возвращает:
        Текст файла PKG-INFO.

    Исключения:
        RuntimeError: если PKG-INFO пуст.
    """
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        member = next(
            item for item in archive.getmembers()
            if item.name.endswith(SDIST_SUFFIX)
        )
        stream = archive.extractfile(member)
        if stream is None:
            raise RuntimeError("пустой PKG-INFO в sdist")
        payload = stream.read()
    return payload.decode(DEFAULT_ENCODING, DECODE_ERRORS)


def _parse_requires_dist(metadata: str) -> list[str]:
    """Разобрать строки Requires-Dist, пропуская optional-extra.

    Аргументы:
        metadata: текст METADATA или PKG-INFO.

    Возвращает:
        Отсортированный список имён прямых зависимостей.
    """
    dependencies: set[str] = set()
    for line in metadata.splitlines():
        if not line.lower().startswith(REQUIRES_DIST_PREFIX):
            continue
        spec = line.split(":", 1)[1].strip()
        if EXTRA_MARKER in spec:
            continue
        match = _SPEC_RE.match(spec)
        if match:
            dependencies.add(match.group(1).lower())
    return sorted(dependencies)


def _pick_files(meta: dict) -> tuple[str | None, str | None]:
    """Выбрать ссылки на wheel и sdist из метаданных PyPI.

    Аргументы:
        meta: разобранный JSON-ответ PyPI.

    Возвращает:
        Кортеж (wheel_url, sdist_url); любой элемент может быть None.
    """
    wheel_url: str | None = None
    sdist_url: str | None = None
    for item in meta.get("urls", []):
        kind = item["packagetype"]
        if kind == "bdist_wheel" and wheel_url is None:
            wheel_url = item["url"]
        elif kind == "sdist" and sdist_url is None:
            sdist_url = item["url"]
    return wheel_url, sdist_url


def _load_meta(package: str, repo_url: str) -> dict:
    """Загрузить и разобрать JSON-метаданные пакета.

    Аргументы:
        package: имя пакета.
        repo_url: базовый URL репозитория.

    Возвращает:
        Словарь с метаданными PyPI.

    Исключения:
        RuntimeError: при ошибке загрузки.
    """
    base = repo_url.rstrip("/") + f"/{package}/json"
    try:
        raw = _download(base, HTTP_TIMEOUT_SHORT_SEC)
    except Exception as exc:
        raise RuntimeError(
            f"не удалось загрузить метаданные PyPI: {exc}"
        ) from exc
    return json.loads(raw)


def fetch_direct_dependencies(
    package: str,
    repo_url: str,
) -> list[str]:
    """Вернуть отсортированные прямые зависимости пакета.

    Аргументы:
        package: имя пакета.
        repo_url: базовый URL репозитория.

    Возвращает:
        Список имён прямых зависимостей.

    Исключения:
        RuntimeError: если пакет не удаётся разрешить.
    """
    meta = _load_meta(package, repo_url)
    wheel_url, sdist_url = _pick_files(meta)
    if wheel_url is None and sdist_url is None:
        raise RuntimeError(f"нет файлов дистрибутива для {package}")

    if wheel_url is not None:
        raw = _download(wheel_url, HTTP_TIMEOUT_LONG_SEC)
        metadata = _read_wheel_metadata(raw)
    else:
        assert sdist_url is not None
        raw = _download(sdist_url, HTTP_TIMEOUT_LONG_SEC)
        metadata = _read_sdist_metadata(raw)

    return _parse_requires_dist(metadata)
