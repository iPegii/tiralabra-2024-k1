import heapq
import math
import random
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

def main():
    graph = get_graph()

    first_node = random.choice(list(graph.nodes))
    second_node = random.choice(list(graph.nodes))

    distances = a_star(first_node, second_node, graph)
    loop_point = second_node
    route = []
    while loop_point is not first_node:
        if distances[loop_point] == loop_point:
            break
        previous_node = distances[loop_point]
        route.append(previous_node)
        loop_point = previous_node

    route = nx.shortest_path(graph, source=first_node, target=second_node,
    weight='time_travel', method='dijkstra')


    color_list = ['green', 'green', 'green', 'green', 'red',
                   'green', 'green', 'green', 'green', 'green', 'green', 'green', 'red', 'red']

    # getting coordinates of the nodes
    # we will store the longitudes and latitudes in following list
    routes_routes = []
    i = 0
    while i < len(route)-1:
        routes_routes.append([route[i], route[i+1]])
        i += 1

    fig, ax = ox.plot_graph_routes(graph, routes_routes, 
                                    save=True,  show=False, close=False,
                                    edge_linewidth=1, node_size=10, route_color = color_list)
    plt.show()

def get_list_of_nodes(graph):
    return list(graph.nodes)

def get_graph():
    graph = ox.graph_from_point((60.1704,24.9412), dist=1000, network_type='drive')
    graph = ox.speed.add_edge_speeds(graph)
    graph = ox.speed.add_edge_travel_times(graph)
    return graph

def process_map(graph):
    """
    Yhdistetään risteyksien solmuja. Risteyksissä voi olla jokaista suuntaa kohden yksi solmu,
    joka johtaa siihen että 4 suunnan risteyksestä voi tulla yhteensä 8 
    vaikka suuntia pitäisi olla 4 ja solmuja 1.

    Yhdistämme risteyksien solmut, jotka ovat 15m päässä toisistaan.
    """

    map_with_intersections_merged = ox.consolidate_intersections(
        graph, tolerance=10, rebuild_graph=True, dead_ends=True,reconnect_edges=True)
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
    prev = {}
    for node in list(graph.nodes):
        if node == start:
            distance[node] = 0
            visited[node] = False
            prev[node] = 0
            continue
        visited[node] = False
        distance[node] = math.inf
        prev[node] = -1

    heap = []
    starting_node = (0,start)

    heapq.heappush(heap,starting_node)
    while len(heap) > 0:

        node = heapq.heappop(heap)[1]
        if visited[node]:
            continue
        visited[node] = True
        for edge in graph[node]:
            travel_time = graph[node][edge][0]["travel_time"]
            going_to = edge
            current = distance[going_to]
            new = None
            if math.isinf(distance[node]):
                new = travel_time
            else:
                new = distance[node]+travel_time
            if new < current:
                distance[going_to] = new
                heapq.heappush(heap,(new,going_to))
                prev[going_to] = node
    return prev

def get_nearest_node(graph,marker):
    nearest_node = ox.nearest_nodes(graph, X=marker.location, Y=marker.location)
    return nearest_node

main()
