import pygame
import random

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetrominos
tetrominos = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6],
     [6, 6]],

    [[7, 7, 7, 7]]
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Define colors
colors = {
    1: (255, 0, 0),
    2: (0, 255, 0),
    3: (0, 0, 255),
    4: (255, 255, 0),
    5: (255, 0, 255),
    6: (0, 255, 255),
    7: (255, 165, 0)
}

def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x, y, colors[cell])

def new_piece():
    piece = random.choice(tetrominos)
    return piece, 0, 3

def valid_position(piece, grid, offset):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                if y + offset[0] >= GRID_HEIGHT or x + offset[1] < 0 or x + offset[1] >= GRID_WIDTH or grid[y + offset[0]][x + offset[1]]:
                    return False
    return True

def merge(grid, piece, offset):
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                grid[y + offset[0]][x + offset[1]] = cell

def clear_lines(grid):
    lines_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
    return lines_cleared

def rotate(piece):
    return [list(row) for row in zip(*reversed(piece))]

# Main loop
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
piece, piece_y, piece_x = new_piece()
game_over = False

while not game_over:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_position(piece, grid, (piece_y, piece_x - 1)):
                piece_x -= 1
            elif event.key == pygame.K_RIGHT and valid_position(piece, grid, (piece_y, piece_x + 1)):
                piece_x += 1
            elif event.key == pygame.K_DOWN and valid_position(piece, grid, (piece_y + 1, piece_x)):
                piece_y += 2
            elif event.key == pygame.K_RETURN:
                rotated_piece = rotate(piece)
                if valid_position(rotated_piece, grid, (piece_y, piece_x)):
                    piece = rotated_piece

    if valid_position(piece, grid, (piece_y + 1, piece_x)):
        piece_y += 1
    else:
        merge(grid, piece, (piece_y, piece_x))
        lines_cleared = clear_lines(grid)
        if lines_cleared:
            print(f"Lines cleared: {lines_cleared}")
        piece, piece_y, piece_x = new_piece()
        if not valid_position(piece, grid, (piece_y, piece_x)):
            game_over = True

    # Draw current piece
    for y, row in enumerate(piece):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x + piece_x, y + piece_y, WHITE)

    # Draw grid
    draw_grid(grid)

    pygame.display.flip()
    clock.tick(3)  # Adjust the speed of the game

pygame.quit()
