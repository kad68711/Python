import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic (estimated cost from current node to end node)
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

def astar_search(graph, start, end):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    end_node = Node(end)
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node)

        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        for neighbor in graph[current_node.position]:
            neighbor_node = Node(neighbor, current_node)
            if neighbor_node in closed_set:
                continue

            neighbor_node.g = current_node.g + 1  # Assuming each step costs 1
            neighbor_node.h = abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])  # Manhattan distance heuristic
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if any(node.position == neighbor_node.position and node.f < neighbor_node.f for node in open_list):
                continue

            heapq.heappush(open_list, neighbor_node)
        # print(neighbor_node.f)


    return None  # No path founde

# Example usage:
graph = {
    (0, 0): [(0, 1), (1, 0)],
    (0, 1): [(0, 0), (1, 1)],
    (1, 0): [(0, 0), (1, 1)],
    (1, 1): [(0, 1), (1, 0), (2, 1)],
    (2, 1): [(1, 1), (2, 2)],
    (2, 2): [(2, 1)]
}

start = (0, 0)
end = (2, 2)

path = astar_search(graph, start, end)
if path:
    print("Shortest path:", path)
else:
    print("No path found.")





