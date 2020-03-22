import pygame
from Node import Node

# setup
# colors for grid
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# size of blocks
WIDTH = 10
HEIGHT = 10
BLOCK_NUM = 30
MARGIN = 5

grid = [[0 for x in range(BLOCK_NUM)] for y in range(BLOCK_NUM)]
red_coords = [[2, 2], [BLOCK_NUM-3, BLOCK_NUM-3]] # here just to save time of searching for start and end
grid[red_coords[0][0]][red_coords[0][1]] = 2
grid[red_coords[1][0]][red_coords[1][1]] = 2

pygame.init()
WINDOW_SIZE = [450, 500]
Screen = pygame.display.set_mode(WINDOW_SIZE)

def isValid(coord):
    if coord[0] > 0 and coord[0] < BLOCK_NUM and coord[1] > 0 and coord[1] < BLOCK_NUM:
        return True
    return False

def isBarrier(board, coord):
    if board[coord[0]][coord[1]] == 1:
        return True
    return False

# check these two
def showFinalPath(current):
    while current is not None:
        grid[current.position[0]][current.position[1]] = 3
        if current.parent is not None:
            print("{} -> {}".format(current.position, current.parent.position))
        else:
            print("{} -> {}".format(current.position, None))
        current = current.parent

def updateBoard(grid, visited):
    for node in visited:
        # position = board[node.position[0]][node.position[1]]
        pygame.draw.rect(Screen, YELLOW, [(MARGIN+WIDTH) * node.position[1] + MARGIN, (MARGIN + HEIGHT) * node.position[0] + MARGIN, WIDTH, HEIGHT])
    pygame.display.update()

def a_star(board):
    cost = 1

    start_node = Node(None, red_coords[0])
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, red_coords[1])
    end_node.g = end_node.h = end_node.f = 0

    domain = []
    visited = []

    domain.append(start_node)

    while len(domain) > 0:
        current_node = domain[0]
        current_index = 0
        for index, node in enumerate(domain):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # Pop current off open list, add to closed list
        domain.pop(current_index)
        visited.append(current_node)
        updateBoard(board, visited)
        if current_node == end_node:
            showFinalPath(current_node)
            return
        
        children = []
        moves = [(0, 1),
                (1, 1),
                (1, 0),
                (1, -1),
                (0, -1),
                (-1, -1),
                (-1, 0)]

        for move in moves:
            node_position = (current_node.position[0] + move[0], current_node.position[1] + move[1])

            if (not isValid(node_position)) and (isBarrier(board, node_position)):
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            for closed_child in visited:
                if child == closed_child:
                    continue

            child.g = current_node.g + cost
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in domain:
                if child == open_node and child.g > open_node.g:
                    continue
            domain.append(child)


def show_board():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            return

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > 10 and pos[0] < 110 and pos[1] > 460 and pos[1] < 495:
                a_star(grid)
                show_board()
            else:
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if grid[row][column] == 0:
                    grid[row][column] = 1
                    print("Barrier added at ({}, {})".format(row, column))
                elif grid[row][column] == 1:
                    grid[row][column] = 0
                    print("({}, {}) color reverted".format(row, column))
                else:
                    print("Cannot put barrier on start or end")

        Screen.fill(BLACK)

        for row in range(BLOCK_NUM):
            for column in range(BLOCK_NUM):
                color = WHITE
                if grid[row][column] == 1:
                    color = GREEN
                elif grid[row][column] == 2:
                    color = RED
                elif grid[row][column] == 3:
                    color = BLUE
                pygame.draw.rect(Screen, color, [(MARGIN+WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        pygame.draw.rect(Screen, (220, 220, 220), [10, 460, 100, 30])
        font = pygame.font.SysFont(None, 20)
        text = font.render("Run A* Search", True, (0, 0, 0))
        Screen.blit(text, (12, 470))
        text = font.render("Click square to set barrier", True, (255, 255, 255))
        Screen.blit(text, (120, 470))

        pygame.display.update()

pygame.quit()