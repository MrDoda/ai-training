import pygame
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, BOTTOM_BAR_HEIGHT, CELL_SIZE, ROW_CELLS, CANVAS_BG_COLOR, BOTTOM_BAR_BG_COLOR, ALIVE_COLOR, DEAD_COLOR
from button import ButtonManager
from life import step 

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = CELL_SIZE
        self.row_cells = ROW_CELLS
        self.canvas_height = WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT
        self.max_rows = self.canvas_height // self.cell_size
        self.history = []
        initial_row = [random.choice([0, 1]) for _ in range(self.row_cells)]
        self.history.append(initial_row)

        self.button_manager = ButtonManager(WINDOW_WIDTH, WINDOW_HEIGHT, BOTTOM_BAR_HEIGHT)
        self.button_manager.set_callback("one", self.generate_one)
        self.button_manager.set_callback("fifty", self.generate_fifty)

    def generate_one(self):
        self.generate_generations(1)

    def generate_fifty(self):
        self.generate_generations(50)

    def generate_generations(self, count):
        for _ in range(count):
            new_row = step(self.history[-1])
            self.history.append(new_row)
        if len(self.history) > self.max_rows:
            self.history = self.history[-self.max_rows:]

    def handle_events(self, events):
        for event in events:
            self.button_manager.handle_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, CANVAS_BG_COLOR, (0, 0, WINDOW_WIDTH, self.canvas_height))
        for i, row in enumerate(self.history):
            y = i * self.cell_size
            for j, cell in enumerate(row):
                x = j * self.cell_size
                color = ALIVE_COLOR if cell == 1 else DEAD_COLOR
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BOTTOM_BAR_BG_COLOR, (0, self.canvas_height, WINDOW_WIDTH, BOTTOM_BAR_HEIGHT))
        self.button_manager.draw(self.screen)
