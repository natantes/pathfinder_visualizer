
def reconstruct_path(came_from, current, draw, param):
    if param == "astar":
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()
    if param == "bfs":
        for node in came_from:
            node.make_path()
            draw()