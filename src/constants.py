"""Общие константы: отсутствие магических чисел в сравнениях."""

# Коды возврата процесса
EXIT_OK = 0
EXIT_RUNTIME_ERROR = 1
EXIT_INVALID_ARGS = 2

# Сетевые таймауты (секунды)
HTTP_TIMEOUT_SHORT_SEC = 30
HTTP_TIMEOUT_LONG_SEC = 60

# Кодировка и поведение при ошибках декодирования
DEFAULT_ENCODING = "utf-8"
DECODE_ERRORS = "replace"

# Формат вывода порядка загрузки
ORDER_WIDTH = 2

# Формат тестового файла графа
COMMENT_PREFIX = "#"
NODE_SEPARATOR = ":"

# Метаданные пакета
METADATA_SUFFIX = ".dist-info/METADATA"
SDIST_SUFFIX = "PKG-INFO"
REQUIRES_DIST_PREFIX = "requires-dist:"
EXTRA_MARKER = "extra =="

# Расширения файлов
PNG_SUFFIX = ".png"
D2_SUFFIX = ".d2"
LAYOUT_FILE = "layout.d2"
EXTRA_MARKER = "extra =="
PNG_SUFFIX = ".png"
D2_SUFFIX = ".d2"
LAYOUT_FILE = "layout.d2"
