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
    return graph.nodes


def get_graph(coordinates, network_type):
    # coordinates: {point,bbox}
    # point:  {latitude, longitude, distance}
    # bbox: {north,east,south,west}
    # network_type: string
    graph = None
    if coordinates["point"]:
        point = coordinates["point"]
        graph = ox.graph_from_point(
            (point["latitude"],
             point["longitude"]), dist=point["distance"], network_type=network_type)
    elif coordinates["bbox"]:
        bbox = coordinates["bbox"]
        graph = ox.graph_from_bbox(
            north=bbox["north"], west=bbox["west"], east=bbox["east"], south=bbox["south"], network_type=network_type)
    print(graph)

    graph = ox.speed.add_edge_speeds(graph)
    graph = ox.speed.add_edge_travel_times(graph)
    return graph


def draw_map(graph):
    ox.plot_graph(graph)


def calculate_travel_time_for_route(graph, route):
    # This calculates time travel for given route
    travel_time = 0
    for i in range(len(route)):
        if i == len(route)-1:
            return travel_time
        nodeNumber = route[i]
        nodeDetail = graph[nodeNumber]
        for child_node in nodeDetail:
            if child_node == route[i+1]:
                travel_time += graph[nodeNumber][child_node][0]["travel_time"]


def show_route(graph, route, route_name):
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
                                     edge_linewidth=1, node_size=10, route_color=color_list)

    image1 = get_image_path(route_name)
    fig1.savefig(image1, dpi=300)
    plt.close(fig1)
