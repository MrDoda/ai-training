import argparse
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game

def main():
    parser = argparse.ArgumentParser(description="Schelling's Model Simulation")
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.5,
        help="Satisfaction threshold for agents (e.g. 0.3 for 30%%, default is 0.5)"
    )
    args = parser.parse_args()

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Schelling's Model Simulation")
    clock = pygame.time.Clock()

    game = Game(screen, threshold=args.threshold)

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
