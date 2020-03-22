import pygame
# setup
# colors for grid
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
    if coord[0] > 0 and coord[0] < BLOCK_NUM-1 and coord[1] > 0 and coord[1] > BLOCK_NUM:
        return True
    return False

def isBarrier(board, coord):
    if board[coord[0]][coord[1]] == 1:
        return True
    return False

def a_star(board):
    cost = 1
    start = red_coords[0]
    target = red_coords[1]
    final_path = [] # final solution
    domain = [] # nodes that are still being explored
    visited = [] # visited nodes



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
                if grid[row][column] == 2:
                    color = RED
                pygame.draw.rect(Screen, color, [(MARGIN+WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
        pygame.draw.rect(Screen, (220, 220, 220), [10, 460, 100, 30])
        font = pygame.font.SysFont(None, 20)
        text = font.render("Run A* Search", True, (0, 0, 0))
        Screen.blit(text, (12, 470))
        text = font.render("Click square to set barrier", True, (255, 255, 255))
        Screen.blit(text, (120, 470))

        pygame.display.update()

pygame.quit()