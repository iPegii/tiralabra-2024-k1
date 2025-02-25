import osmnx as ox
import matplotlib.pyplot as plt
import os
 

def get_image_path(param):

    project_root = os.path.abspath(os.path.dirname(__file__))

    images_dir = os.path.join(project_root, '../images')

    # Create the 'images' directory if it doesn't exist
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    image_path = os.path.join(project_root, '../images', f'image-{param}.png')
    return image_path


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

def get_nearest_node(graph,marker):
    nearest_node = ox.nearest_nodes(graph, X=marker.location, Y=marker.location)
    return nearest_node

def show_route(graph,route, route_name):
    color_list = ['green', 'green', 'green', 'green', 'red',
                   'green', 'green', 'green', 'green', 'green', 'green', 'green', 'red', 'red']

    # getting coordinates of the nodes
    # we will store the longitudes and latitudes in following list
    routes_routes = []
    i = 0
    while i < len(route)-1:
        routes_routes.append([route[i], route[i+1]])
        i += 1

    fig1, ax1 = ox.plot_graph_routes(graph, routes_routes, 
                                    save=True,  show=False, close=False,
                                    edge_linewidth=1, node_size=10, route_color = color_list)
        
    image1 = get_image_path(route_name)
    fig1.savefig(image1, dpi=300)
    plt.close(fig1)