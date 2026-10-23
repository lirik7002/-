"""Точка входа эмулятора."""
import argparse
import sys

from src.vfs import create_default_vfs
from src.vfs_loader import load_vfs_from_xml
from src.gui import ShellApp
from src.shell import Shell
from src.scripting import run_script

def build_parser() -> argparse.ArgumentParser:
    """Создаёт CLI-парсер."""
    p = argparse.ArgumentParser(description="Эмулятор оболочки ОС")
    p.add_argument("--vfs", help="путь к XML-файлу VFS")
    p.add_argument("--script", help="путь к стартовому скрипту")
    p.add_argument("--debug", action="store_true", help="отладка")
    return p

def main() -> int:
    """Главная функция."""
    args = build_parser().parse_args()

    if args.debug:
        print(f"vfs_path={args.vfs}")
        print(f"script_path={args.script}")

    if args.vfs:
        vfs = load_vfs_from_xml(args.vfs)
    else:
        vfs = create_default_vfs()

    app = ShellApp(Shell(vfs, lambda t: print(t)), title=f"VFS: {vfs.name}")

    if args.script:
        run_script(args.script, app)

    app.run()
    return 0

if __name__ == "__main__":
    sys.exit(main())
