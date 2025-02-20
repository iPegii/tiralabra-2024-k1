import heapq
import random
import math
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

def main():
    graph = get_graph()

    first_node = random.choice(list(graph.nodes))
    second_node = random.choice(list(graph.nodes))

    route_to_goal = a_star(first_node, second_node, graph)

    print(route_to_goal)

    route = nx.shortest_path(graph, source=first_node, target=second_node,
    weight='time_travel', method='dijkstra')
    print(f"A-star route length: {len(route_to_goal)}")
    print(f"A-star route: {route_to_goal}")
    print("")
    print("-------------------------")
    print("")
    print(f"djikstra route length: {len(route)}")
    print(f"djikstra route: {route}")



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

class Node:
    def __init__(self, distance, number, prev_route):
        """
        distance: Int
        number: Int
        prev_route: Int[]
        """
        self.distance = distance # etäisyys tähän nodeen asti
        self.number = number # Osoite
        self.prev_route = prev_route # Pidetään lista reitistä tälle nodelle asti
    def __str__(self):
        str = ""
        for i in self.prev_route:
            print(i)
            if(len(str) == 0):
                str = f"{i}"
            str += f"--> {i}"
        return str
    def __lt__(self, other):
        return self.distance < other.distance
    
def euclidean_distance(graph, first_node, second_node):
    first_lon = graph.nodes[first_node]["x"] # pituusaste
    first_lat = graph.nodes[first_node]["y"] # leveysaste

    second_lon = graph.nodes[second_node]["x"] # pituusaste
    second_lat = graph.nodes[second_node]["y"] # leveysaste

    return math.sqrt((second_lon - first_lon)**2 + (second_lat - first_lat)**2)

def a_star(start, goal, graph):
    """Parametrit:
    start = aloituspiste, josta algoritmi aloittaa matkan
    goal = päätöspiste, johon algoritmilla halutaan päästä
    h = algoritmin heuristinen osuus, joka laskee jokaisen solmun hinnan 
    """

    openList =  []
    closedList = {}

    starting_node = Node(0,start,[start])

    heapq.heappush(openList,starting_node)
   # print(f"testing {graph[start]['2037356632']}")
    while len(openList) > 0:

        node = heapq.heappop(openList)
        if closedList.get(node.number):
            continue
        if node.number == goal:
            print("goal")
            return node.prev_route
        for child_node in graph[node.number]:
            print("child_node: ", child_node)
            travel_time = graph[node.number][child_node][0]["travel_time"]
            new_node = None
            new_route = node.prev_route + [child_node]
            if closedList.get(child_node) is not None:
                # Jos closedList sisältää jo noden niin katsotaan onko nykyinen reitti nopeampi

                current_distance_to_child = closedList.get(child_node).distance
                euclidean_distance_to_goal = euclidean_distance(graph,child_node,goal)

                new_distance_to_child = node.distance + travel_time + euclidean_distance_to_goal

                if new_distance_to_child < current_distance_to_child:
                    new_route = node.prev_route + [child_node]
                    new_node = Node(new_distance_to_child,child_node,new_route)
                else:
                    continue
            else:
                new_distance_to_child = node.distance+travel_time
                new_node = Node(new_distance_to_child,child_node,new_route)
            heapq.heappush(openList,new_node)
        closedList[node.number] = node
    

def get_nearest_node(graph,marker):
    nearest_node = ox.nearest_nodes(graph, X=marker.location, Y=marker.location)
    return nearest_node

main()
