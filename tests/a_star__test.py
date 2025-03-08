from src.graph.route import get_graph,get_list_of_nodes
from networkx import MultiDiGraph
# content of test_sample.py

def test_get_graph():
    graph = get_graph()
    amount_of_nodes = len(graph.nodes)
    amount_of_edges = len(graph.edges)
    assert amount_of_nodes == 418
    assert amount_of_edges == 913
    assert isinstance(graph, MultiDiGraph)

def test_get_list_of_nodes():
    graph = get_graph()
    list_of_nodes = get_list_of_nodes(graph)
    assert list_of_nodes[1514631294]
    assert list_of_nodes[1376293751]
    assert list_of_nodes[1372441183]

# For this test that the file is saved (and maybe more?)
def test_show_route():
    assert 1 == 1