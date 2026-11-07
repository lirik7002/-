import pytest

from src.cli import validate
from src.cli import build_parser


def _ns(**kw):
    base = dict(package="requests", repo="https://pypi.org",
                mode="online", output="out.png", exclude="")
    base.update(kw)
    return build_parser().parse_args([f"--{k}={v}"
                                     for k, v in base.items()])


def test_valid_online():
    assert validate(_ns()) == []


def test_bad_package():
    errs = validate(_ns(package="bad name!"))
    assert any("package" in e for e in errs)


def test_bad_url():
    errs = validate(_ns(repo="not-a-url"))
    assert any("repo" in e for e in errs)


def test_bad_output():
    errs = validate(_ns(output="out.jpeg"))
    assert any("output" in e for e in errs)


def test_test_mode_missing_file(tmp_path):
    errs = validate(_ns(mode="test", repo=str(tmp_path / "nope.txt")))
    assert any("not found" in e for e in errs)
