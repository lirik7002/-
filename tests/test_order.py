from src.order import cyclic_nodes, load_order


def test_simple_diamond():
    g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    order = load_order(g)
    assert order.index("D") < order.index("B")
    assert order.index("D") < order.index("C")
    assert order.index("B") < order.index("A")
    assert order.index("C") < order.index("A")


def test_cycle_detected():
    g = {"A": ["B"], "B": ["A"]}
    assert cyclic_nodes(g) == ["A", "B"] or cyclic_nodes(g) == ["B", "A"]
