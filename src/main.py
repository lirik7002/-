"""Entry point of the depviz tool. Runs all stages in sequence."""

import sys

from src.cli import parse_args, print_config
from src.config import Config
from src.graph import build_from_pypi, build_from_test
from src.order import cyclic_nodes, format_order, load_order
from src.visualize import render_png


def build_graph(cfg: Config) -> dict[str, list[str]]:
    """Build the dependency graph depending on the selected mode."""
    if cfg.mode == "test":
        return build_from_test(cfg.package, cfg.repo, cfg.exclude)
    return build_from_pypi(cfg.package, cfg.repo, cfg.exclude)


def report(graph: dict[str, list[str]]) -> None:
    """Print a human-readable summary of the graph."""
    print("--- Dependency graph ---")
    for node in sorted(graph):
        deps = ", ".join(graph[node]) or "(none)"
        print(f"{node}: {deps}")

    print("\n--- Load order ---")
    print(format_order(load_order(graph)))

    cyc = cyclic_nodes(graph)
    if cyc:
        print("\n--- Cycles detected ---")
        print(", ".join(cyc))


def main(argv: list[str] | None = None) -> int:
    cfg = parse_args(argv)
    print_config(cfg)
    print()

    try:
        graph = build_graph(cfg)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    report(graph)

    try:
        d2_path = render_png(graph, cfg.output)
        print(f"\nD2 source : {d2_path}")
        print(f"PNG image : {cfg.output}")
    except RuntimeError as exc:
        print(f"[WARN] PNG rendering skipped: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
