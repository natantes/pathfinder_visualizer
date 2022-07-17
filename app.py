import pygame
import math
import PySimpleGUI as sg
from bfs import bfs
from dfs import dfs
from astar import *
from astar2 import *
from dijkstra import dijkstra

WIDTH = 800

RED = (255, 0, 0)
GREEN = (118, 255, 97)
BLUE = (0,238,238)
YELLOW = (238,201,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (212, 187, 252)
ORANGE = (130, 0, 172)
GREY = (230,238,245)
TURQUOISE = (25, 146, 252)
gradient = [255, 0, 10]
c = 0
sign = 1
direction = 1

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbor = []
        self.width = width
        self.total_rows = total_rows
        self.border_radius = 5

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color =  ORANGE

    def make_closed(self):
        global c
        c += 1

        global sign
        sign *= -1

        global direction 

        if c == 5:
            if gradient[1] == 240 and gradient[2] == 240:
                direction *= -1
            if gradient[1] == 0 and gradient[2] == 0:
                direction *= -1
            if direction > 0:
                if sign == -1:
                    gradient[1] += 10
                else:
                    gradient[2] += 10
            elif direction < 0:
                if sign == -1:
                    gradient[1] -= 10
                else:
                    gradient[2] -= 10
            c = 0

        self.color = tuple(gradient)

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width), border_radius=5)

    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


sg.theme('LightPurple')


def main_menu():

    font = ("Arial", 14)

    layout = [[sg.Text('Main Menu')],
            [sg.Button('A* Pathfinder (Manhattan Heuristic)')],
            [sg.Button('A* Pathfinder (Euclidean Heuristic)')],
            [sg.Button("Dijkstra's Algorithm Pathfinder")],
            [sg.Button('Breadth First Search Pathfinder')],
            [sg.Button('Depth First Search Pathfinder')],
            [sg.Button('Exit', size=6)]]

    window = sg.Window('MAIN MENU', layout, element_justification='c', font=font)

    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            return "exit"
        if event == 'A* Pathfinder (Manhattan Heuristic)':
            window.close()
            return "a1"
        if event == 'A* Pathfinder (Euclidean Heuristic)':
            window.close()
            return "a2"
        if event == "Dijkstra's Algorithm Pathfinder":
            window.close()
            return "dij"
        if event == 'Breadth First Search Pathfinder':
            window.close()
            return "bfs"
        if event == 'Depth First Search Pathfinder':
            window.close()
            return "dfs"


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (WIDTH, i* gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j* gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):

    pathfinder = None

    while not pathfinder:
        pathfinder = main_menu()

    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Path Finding Algorithm")

    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    
    a_dict = {"a1" : astar, "a2": astar2, "dfs": dfs, "bfs": bfs, "dij": dijkstra}
    
    if pathfinder != "exit":
        while run:
            draw(win, grid, ROWS, width)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if started:
                    continue

                if pygame.mouse.get_pressed()[0]: # left mouse button clicked
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]

                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()

                elif pygame.mouse.get_pressed()[2]: # right mouse button clicked
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for node in row:
                                node.update_neighbors(grid)

                        a_dict[pathfinder](lambda: draw(win, grid, ROWS, width), grid, start, end)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)

    pygame.quit()

WIN = "placeholder"
main(WIN, WIDTH)