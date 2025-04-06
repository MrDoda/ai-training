import pygame
import argparse
import life
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from game import Game

def main():
    parser = argparse.ArgumentParser(description="1D Game of Life with selectable rule")
    parser.add_argument("--rule", type=int, default=-1, help="Specify rule index to use (0-indexed)")
    args = parser.parse_args()
    
    if args.rule >= 0:
        life._selected_rule = args.rule
        print(f"Rule parameter provided: {args.rule}")

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("1D Game of Life")
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
