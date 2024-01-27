import osmnx as ox


def main():
    graph = get_graph()
    # processed_map = process_map(graph)
    draw_map(graph)



def get_graph():
    graph = ox.graph_from_place('Helsinki', network_type='drive')
    return graph

def process_map(graph):
    """
    Yhdistetään risteyksien solmuja. Risteyksissä voi olla jokaista suuntaa kohden yksi solmu,
    joka johtaa siihen että 4 suunnan risteyksestä voi tulla yhteensä 8 
    vaikka suuntia pitäisi olla 4 ja solmuja 1.

    Yhdistämme risteyksien solmut, jotka ovat 15m päässä toisistaan.
    """

    map_with_intersections_merged = ox.consolidate_intersections(
        graph, tolerance=10, rebuild_graph=True, dead_ends=True)
    return map_with_intersections_merged


def draw_map(graph):
    ox.plot_graph(graph)


main()
