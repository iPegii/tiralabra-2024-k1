import heapq
import math
import osmnx as ox
import networkx as nx


def main():
    graph = get_graph()
    # processed_map = process_map(graph)
    graph = ox.speed.add_edge_speeds(graph)
    graph = ox.speed.add_edge_travel_times(graph)
    print(list(graph.nodes))
    #print(list(graph.edges))

    first_node = 25435275
    second_node = 262987538
    print("------------")
    print(graph[262987538])

    a_star(first_node, second_node, graph)

    #  draw_map(graph)



def get_graph():
    graph = ox.graph_from_place('Kallio, Helsinki', network_type='drive')
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

def reconstruct_path(came_from, current):
    total_path = current
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path

def a_star(start, goal, graph):
    """Parametrit:
    start = aloituspiste, josta algoritmi aloittaa matkan
    goal = päätöspiste, johon algoritmilla halutaan päästä
    h = algoritmin heuristinen osuus, joka laskee jokaisen solmun hinnan 
    """

    # (Paino, mikä solmu)
    visited =  {}
    distance = {}

    for node in list(graph.nodes):
        visited[node] = False
        distance[node] = math.inf

    heap = []
    starting_node = (0,start)

    heapq.heappush(heap,starting_node)
    while len(heap) > 0:
        node = heap.pop()[1]
        if visited[node]:
            continue
        visited[node] = True
        for edge in graph[node]:
            print("Edge:")
            travel_time = graph[node][edge][0]["travel_time"]
            print(f"First node : {node}")
            print(f"Second node : {edge}")

            going_to = edge
            current = distance[going_to]
            new = distance[edge]+travel_time
            print(f"New : {new} smaller than {current}")
            if new < current:
                distance[going_to] = new
                heapq.heappush(heap,(new,edge.to))



main()
