import random
import networkx as nx
from algorithm.a_star import a_star
from graph.route import get_graph, show_route, calculate_travel_time_for_route

# north=60.15858, west=24.94148, east=24.95053, south=60.15493, network_type='drive')


def main():
    coordinates = {"point": {"latitude": 60.1704,
                             "longitude": 24.9412, "distance": 1000}}
    graph = get_graph(coordinates, "drive")
    print(graph.nodes)
    first_node = random.choice(list(graph.nodes))
    second_node = random.choice(list(graph.nodes))

    goal_node = a_star(first_node, second_node, graph)

    route_to_goal = goal_node.prev_route
    distance_to_goal = goal_node.distance  # distance in time travel

    print(route_to_goal)

    travel_time = nx.shortest_path_length(
        graph, first_node, second_node, weight='travel_time')
    print(round(travel_time))

    osmnx_route = nx.shortest_path(graph, source=first_node, target=second_node,
                                   weight='time_travel', method='dijkstra')

    # Printing related stuff, debugging etc.
    print(f"A-star route length: {len(route_to_goal)}")
    print(f"A-star route travel time: {distance_to_goal}")
    print(f"A-star route: {route_to_goal}")
    print("")
    print("-------------------------")
    print("")
    print(f"djikstra route length: {len(osmnx_route)}")
    print(
        f"djikstra travel time: {calculate_travel_time_for_route(graph, osmnx_route)}")
    print(f"djikstra route: {osmnx_route}")

    show_route(graph, osmnx_route, "djikstra-route")
    show_route(graph, route_to_goal, "a-star-route")

    # plt.show() <-- does not work on linux by default


main()
