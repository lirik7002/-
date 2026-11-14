"""Генерация D2-описания графа и рендер в PNG."""
import subprocess

D2_HEADER = "direction: right\n"


def to_d2(edges):
    """Формирует текст на языке D2."""
    lines = [D2_HEADER]
    for src, dst in edges:
        lines.append(f'"{src}" -> "{dst}"\n')
    return "".join(lines)


def render_png(d2_text, output_path):
    """Рендерит D2 в PNG через d2 CLI."""
    src = output_path + ".d2"
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(d2_text)
    try:
        subprocess.run(
            ["d2", src, output_path],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError as err:
        raise RuntimeError("d2 CLI не установлен") from err
    except subprocess.CalledProcessError as err:
        raise RuntimeError(f"d2 завершился с ошибкой: {err}") from err
