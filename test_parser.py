from src.parser import parse_command

def test_simple():
    assert parse_command("ls -la") == ("ls", ["-la"])

def test_quotes():
    assert parse_command('cd "my dir"') == ("cd", ["my dir"])

def test_empty():
    assert parse_command("   ") == ("", [])
