"""Command line interface: argument parsing and validation."""

import argparse
import os
import re
import sys
from urllib.parse import urlparse

from src.config import Config
from src.constants import (
    EXIT_INVALID_ARGS,
    PNG_SUFFIX,
)

PACKAGE_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def build_parser() -> argparse.ArgumentParser:
    """Create the argparse parser with all options of the tool."""
    parser = argparse.ArgumentParser(
        prog="depviz",
        description="Visualize pip package dependency graph.",
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Name of the package to analyse",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="PyPI URL or path to a test graph file",
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=["online", "test"],
        help="Work mode: online PyPI or local test file",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output PNG file name",
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Substring; packages containing it are skipped",
    )
    return parser


def _validate_package(name: str) -> list[str]:
    """Return error strings for an invalid package name."""
    if not name or not PACKAGE_RE.match(name):
        return ["package: expected letters, digits, '.', '_', '-'"]
    return []


def _validate_online_repo(repo: str) -> list[str]:
    """Validate PyPI-style URL for the online mode."""
    parsed = urlparse(repo)
    valid = (
        parsed.scheme in ("http", "https") and bool(parsed.netloc)
    )
    if not valid:
        return ["repo: online mode expects an http(s) URL"]
    return []


def _validate_repo(repo: str, mode: str) -> list[str]:
    """Validate the repository argument for the given mode."""
    if mode == "online":
        return _validate_online_repo(repo)
    if not os.path.isfile(repo):
        return [f"repo: test file not found: {repo}"]
    return []


def _validate_output(path: str) -> list[str]:
    """Validate the output PNG file name and its directory."""
    errors: list[str] = []
    if not path.lower().endswith(PNG_SUFFIX):
        errors.append("output: file name must end with .png")
    out_dir = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(out_dir):
        errors.append(f"output: directory does not exist: {out_dir}")
    return errors


def validate(args: argparse.Namespace) -> list[str]:
    """Return a list of human-readable validation errors."""
    errors: list[str] = []
    errors += _validate_package(args.package)
    errors += _validate_repo(args.repo, args.mode)
    errors += _validate_output(args.output)
    return errors


def parse_args(argv: list[str] | None = None) -> Config:
    """Parse argv and exit with error code on invalid input."""
    parser = build_parser()
    args = parser.parse_args(argv)
    errors = validate(args)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}", file=sys.stderr)
        sys.exit(EXIT_INVALID_ARGS)
    return Config(
        package=args.package,
        repo=args.repo,
        mode=args.mode,
        output=args.output,
        exclude=args.exclude,
    )


def print_config(cfg: Config) -> None:
    """Print all user settings as key-value pairs (stage 1)."""
    print(f"package = {cfg.package}")
    print(f"repo    = {cfg.repo}")
    print(f"mode    = {cfg.mode}")
    print(f"output  = {cfg.output}")
    print(f"exclude = {cfg.exclude!r}")
