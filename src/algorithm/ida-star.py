from algorithm.a_star import euclidean_distance, Node
import math

def ida_star(start, goal,graph):
    """Parametrit:
    start = aloituspiste, josta algoritmi aloittaa matkan
    goal = päätöspiste, johon algoritmilla halutaan päästä
    h = algoritmin heuristinen osuus, joka laskee jokaisen solmun hinnan 
    """
    threshold = euclidean_distance(graph,start,goal)*10
    start_node = Node(0, start, [])
    while True:
        current_path = search(graph, start_node, goal, threshold, cost=0)
        if current_path[0] == True:
            return current_path
        if current_path[1] == math.inf:
            return (False, current_path[1],current_path[2])
        threshold = current_path[1]

def search(graph, node, goal, threshold, cost):
    f = cost+euclidean_distance(graph, node.number, goal)
    if f > threshold:
        return (False, f,node)
    if node.number == goal:
        print("goal founded: ", node)
        return (True, f,node)
    min = math.inf
    for child_node in graph[node.number]:
        travel_length = graph[node.number][child_node][0]["length"]
        travel_time = graph[node.number][child_node][0]["travel_time"]
        new_route = node.prev_route + [child_node]
        child_node_object = Node(travel_time,child_node,new_route)
        temp = search(graph, child_node_object, goal, threshold, cost + euclidean_distance(graph,child_node,goal))
        if temp[0] == True:
            print("goal founded, child: ", temp[1])
            return (True, min,temp[2])
        if temp[1] < min:
                print("better", child_node)
                min = temp[1]
    return (False, min,node)