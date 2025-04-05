import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Schelling's Model Simulation")
    clock = pygame.time.Clock()
    game = Game(screen)
    running = True
    while running:
        events = pygame.event.get()
        game.handle_events(events)
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
