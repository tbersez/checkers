import sys
import pygame; pygame.init()
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def clickToBoardCoordinates() -> tuple:
    """
    Return coords (row, col) from a click in the window.
    """
    pixelCoords = pygame.mouse.get_pos()
    return (pixelCoords[0] // SQUARE_SIZE, pixelCoords[1] // SQUARE_SIZE)

def main():
    run = True
    clock = pygame.time.Clock()

    game = Game(win = WIN)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = clickToBoardCoordinates()
                print(coords)
                game.runGame(coords)
        
        game.updateGui()
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()