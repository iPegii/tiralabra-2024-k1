import math
import heapq
import math

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
    while len(openList) > 0:

        node = heapq.heappop(openList)
        if closedList.get(node.number):
            continue
        if node.number == goal:
            return node
        for child_node in graph[node.number]:
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