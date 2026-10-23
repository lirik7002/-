"""Исполнитель стартового скрипта."""
def run_script(path: str, app) -> None:
    """Выполняет команды из скрипта.

    Комментарии — строки с `#`. При ошибке сообщает и продолжает.
    """
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            app.echo(f"> {line}")
            try:
                result = app.shell.execute(line)
                if result:
                    app.echo(result)
            except Exception as exc:
                app.echo(f"[script error, line {lineno}]: {exc}")
