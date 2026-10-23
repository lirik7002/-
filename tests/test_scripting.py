from src.scripting import run_script
from src.shell import Shell
from src.vfs import create_default_vfs

class FakeApp:
    def __init__(self):
        self.lines = []
        self.shell = Shell(create_default_vfs(), self.echo)

    def echo(self, text):
        self.lines.append(text)

def test_script_continues_on_error(tmp_path):
    script = tmp_path / "s.txt"
    script.write_text("# c\nunknown_cmd\nls\n", encoding="utf-8")
    app = FakeApp()
    run_script(str(script), app)
    assert any("script error" in line for line in app.lines)
    assert any("home" in line for line in app.lines)
