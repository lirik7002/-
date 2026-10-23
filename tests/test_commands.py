from src.vfs import create_default_vfs
from src.commands import mkdir, touch, ls

def test_mkdir():
    vfs = create_default_vfs()
    mkdir.Command().run(vfs, ["/newdir"])
    assert "newdir" in vfs.root.children

def test_touch():
    vfs = create_default_vfs()
    touch.Command().run(vfs, ["/home/a.txt"])
    assert "a.txt" in vfs.root.children["home"].children
