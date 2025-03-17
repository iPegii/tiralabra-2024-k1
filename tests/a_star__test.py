from src.graph.route import get_graph, get_list_of_nodes
from networkx import MultiDiGraph
# content of test_sample.py

TEST_COORDINATES = {"bbox": {"north": 60.15858,
                             "west": 24.94148, "east": 24.95053, "south": 60.15493}}


def test_get_graph():
    graph = get_graph(TEST_COORDINATES, "drive")
    amount_of_nodes = len(graph.nodes)
    amount_of_edges = len(graph.edges)
    assert amount_of_nodes == 24
    assert amount_of_edges == 68
    assert isinstance(graph, MultiDiGraph)


def test_get_list_of_nodes():
    graph = get_graph(TEST_COORDINATES, "drive")
    list_of_nodes = get_list_of_nodes(graph)
    assert list_of_nodes[25469526]
    assert list_of_nodes[1379511234]
    assert list_of_nodes[1379511271]

# For this test that the file is saved (and maybe more?)


def test_show_route():
    coordinates = {"bbox": {"north": 60.15858,
                            "west": 24.94148, "east": 24.95053, "south": 60.15493}}
    graph = get_graph(coordinates, "drive")
    assert 1 == 1
