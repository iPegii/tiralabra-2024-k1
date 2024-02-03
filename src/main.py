import heapq
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

def reconstruct_path(came_from, current):
    total_path = current
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path

def a_star(start, goal, h):
    """Parametrit:
    start = aloituspiste, josta algoritmi aloittaa matkan
    goal = päätöspiste, johon algoritmilla halutaan päästä
    h = algoritmin heuristinen osuus, joka laskee jokaisen solmun hinnan 
    """

    #open_set sisältää tiedetyt solmut, joita voi laajentaa
    open_set = [start]

    came_from = []

    currently_cheapest_to_n = []
    currently_cheapest_to_n[start] = 0

    forecasted_cheapest_path =[]
    forecasted_cheapest_path[start] = h(start)

    while len(open_set) > 0:
        current = heapq.nsmallest(1, open_set, key=None)
        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        for neighbour in current:
            weight_to_neighbour = 1 # but here weight between them
         #   """Distance from start -> current -> neighbour"""
            distance_to_neighbour = currently_cheapest_to_n[current] + weight_to_neighbour
            if distance_to_neighbour < currently_cheapest_to_n[neighbour]:
                came_from[neighbour] = current
                currently_cheapest_to_n[neighbour] = forecasted_cheapest_path
                forecasted_cheapest_path[neighbour] = forecasted_cheapest_path + h(neighbour)
                if neighbour not in open_set:
                    heapq.heappush(open_set, (neighbour))

    return False



main()
