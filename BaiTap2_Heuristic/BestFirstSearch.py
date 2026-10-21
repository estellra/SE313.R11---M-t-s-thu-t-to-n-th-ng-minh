
import heapq

def greedy_bfs(graph, heuristics, start, goal):
    frontier = []
    heapq.heappush(frontier, (heuristics[start], start))

    came_from = {start: None}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = came_from[curr]
            return path[::-1]

        for neighbor, _ in graph.get(current, []):
            if neighbor not in came_from and neighbor in heuristics:
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristics[neighbor], neighbor))

    return None


def input_data():
    heuristics = {}
    graph = {}

    while True:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        if len(parts) == 2:
            try:
                node, h_val = parts[0], float(parts[1])
                heuristics[node] = h_val
                if node not in graph:
                    graph[node] = []
            except ValueError:
                pass

    while True:
        line = input().strip()
        if not line:
            break
        parts = line.split()
        if len(parts) == 3:
            try:
                u, v, cost = parts[0], parts[1], float(parts[2])
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append((v, cost))
            except ValueError:
                pass

    start = input().strip()
    goal = input().strip()

    return graph, heuristics, start, goal


if __name__ == "__main__":
    graph, heuristics, start, goal = input_data()
    path = greedy_bfs(graph, heuristics, start, goal)

    if path:
        print("Đường đi tìm được:", " -> ".join(path))
    else:
        print("None")
