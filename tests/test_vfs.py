import pytest
from src.vfs import create_default_vfs

def test_default():
    vfs = create_default_vfs()
    assert vfs.name == "default-vfs"
    assert "home" in vfs.root.children

def test_resolve():
    vfs = create_default_vfs()
    node = vfs.resolve("/home")
    assert node.name == "home"

def test_missing():
    vfs = create_default_vfs()
    with pytest.raises(FileNotFoundError):
        vfs.resolve("/nope")
