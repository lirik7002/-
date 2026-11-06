"""Shared constants: no magic numbers in comparisons."""

# Exit codes
EXIT_OK = 0
EXIT_RUNTIME_ERROR = 1
EXIT_INVALID_ARGS = 2

# Network
HTTP_TIMEOUT_SHORT_SEC = 30
HTTP_TIMEOUT_LONG_SEC = 60

# Encoding
DEFAULT_ENCODING = "utf-8"
DECODE_ERRORS = "replace"

# Output formatting
ORDER_WIDTH = 2

# Test graph
COMMENT_PREFIX = "#"
NODE_SEPARATOR = ":"

# Metadata
METADATA_SUFFIX = ".dist-info/METADATA"
SDIST_SUFFIX = "PKG-INFO"
REQUIRES_DIST_PREFIX = "requires-dist:"
EXTRA_MARKER = "extra =="
PNG_SUFFIX = ".png"
D2_SUFFIX = ".d2"
LAYOUT_FILE = "layout.d2"
