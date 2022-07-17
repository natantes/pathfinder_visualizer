
import pygame
from reconstruct_path import *

def bfs(draw, grid, start, end):

    queue = [(start, [start])]
    visited = set()

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current, path = queue.pop(0)
        visited.add(current)

        for neighbor in current.neighbors:
            if neighbor == end:
                reconstruct_path(path, end, draw, "bfs")
                end.make_end()
                start.make_start()
                return True
            else:
                if neighbor not in visited:
                    neighbor.make_open()
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        draw()

        if current != start:
            current.make_closed()

    return False