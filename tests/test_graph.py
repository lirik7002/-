from src.graph import bfs_graph


def _get(d):
    return lambda n: d.get(n, [])


def test_simple_chain():
    g = {"A": ["B"], "B": ["C"], "C": []}
    res = bfs_graph("A", _get(g))
    assert set(res) == {"A", "B", "C"}
    assert res["B"] == ["C"]


def test_cycle_terminates():
    g = {"A": ["B"], "B": ["A"]}
    res = bfs_graph("A", _get(g))
    assert set(res) == {"A", "B"}


def test_filter_skips_subtree():
    g = {"A": ["B", "Xdev"], "B": [], "Xdev": ["Y"]}
    res = bfs_graph("A", _get(g), exclude="dev")
    assert "Xdev" not in res
    assert "Y" not in res
