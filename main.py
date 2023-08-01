import pygame
from checkers.constants import WIDTH, HEIGHT
from checkers.board import Board

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        # Board initialisation
        board = Board()
        board.initialiseBoard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        board.renderBoard(WIN)
        pygame.display.update()

    pygame.quit()
main()