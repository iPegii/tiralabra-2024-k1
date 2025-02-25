import random
import networkx as nx
from algorithm.a_star import a_star
from graph.route import get_graph, show_route
 

def main():
    graph = get_graph()
    print(graph.nodes['298368071'])

    first_node = random.choice(list(graph.nodes))
    second_node = random.choice(list(graph.nodes))

    goal_node = a_star(first_node, second_node, graph)

    route_to_goal = goal_node.prev_route
    distance_to_goal = goal_node.distance # distance in time travel

    print(route_to_goal)

    travel_time = nx.shortest_path_length(graph, first_node, second_node, weight='travel_time')
    print(round(travel_time))

    route = nx.shortest_path(graph, source=first_node, target=second_node,
    weight='time_travel', method='dijkstra')



    # Printing related stuff, debugging etc.
    print(f"A-star route length: {len(route_to_goal)}")
    print(f"A-star route: {route_to_goal}")
    print("")
    print("-------------------------")
    print("")
    print(f"djikstra route length: {len(route)}")
    print(f"djikstra route: {route}")

    show_route(graph,route,"djikstra-route")
    show_route(graph,route_to_goal,"a-star-route")

    #plt.show() <-- does not work on linux by default


main()
