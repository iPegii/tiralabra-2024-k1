from a_star import Node, euclidean_distance
import heapq

def heuristic(node):
    print("wow")


def ida_star(graph, start, goal):
    """Parametrit:
    start = aloituspiste, josta algoritmi aloittaa matkan
    goal = päätöspiste, johon algoritmilla halutaan päästä
    h = algoritmin heuristinen osuus, joka laskee jokaisen solmun hinnan 
    """
    threshold = 0
    path_list = []
    start_node = Node(0,start,[])

    heapq.heappush(path_list,start_node)
    while True:
        current_path = search(graph,start_node, goal, threshold, path_list, cost=0)

        if current_path:
            return current_path
        if current_path == "INF":
            return False
        threshold = current_path

def search(graph, node, goal, threshold, path_list, cost):
    current_node = heapq.heappop(path_list)
    f = cost+euclidean_distance(graph,current_node,goal)
    if f > threshold:
        return f
    if current_node == goal:
        return True