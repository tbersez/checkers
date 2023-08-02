import pygame

# GAME
ROWS, COLS = 8, 8
PIECES_ROWS = 3 # How many rows of pieces each player has when the game begins
PLAYER_RED = 0 # Player red starts
PLAYER_WHITE = 1

# GUI
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE =  WIDTH // COLS

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (245, 245, 222)
GREEN = (0, 51, 0)
RED = (153, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# PICS
CROWN = pygame.transform.scale(
    pygame.image.load('pics/crown.png'),
    (SQUARE_SIZE, SQUARE_SIZE)
)
