import pygame
import random
from config import AUTO_FPS, WINDOW_WIDTH, WINDOW_HEIGHT, BOTTOM_BAR_HEIGHT, GRAPH_AREA_X, GRAPH_AREA_Y, GRAPH_AREA_WIDTH, GRAPH_AREA_HEIGHT, GRID_ROWS, GRID_COLS
from button import ButtonManager
import schelling

class Game:
    def __init__(self, screen, threshold):
        self.number_of_iterations = 0
        self.fully_satisfied = False
        self.screen = screen
        self.threshold = threshold
        self.rep = schelling.initialize_representation(density=0.9)
        self.total_agents = sum(1 for i in range(GRID_ROWS) for j in range(GRID_COLS) if self.rep[i][j] != 0)
        self.evolution = []
        self.button_manager = ButtonManager(WINDOW_WIDTH, WINDOW_HEIGHT, BOTTOM_BAR_HEIGHT)
        self.button_manager.set_callback("1 Step", self.one_step)
        self.button_manager.set_callback("10 Steps", self.ten_steps)
        self.button_manager.set_callback("AUTO", self.toggle_auto)
        self.auto_mode = False
        self.frame_count = 0

    def compute_satisfaction_ratio(self):
        satisfied = 0
        occupied = 0
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                if self.rep[i][j] != 0:
                    occupied += 1
                    if schelling.is_satisfied(self.rep, i, j, threshold=self.threshold):
                        satisfied += 1
        satisfaction = satisfied / occupied if occupied > 0 else 1.0
        if satisfaction == 1.0:
            self.fully_satisfied = True
            print(f"Fully satisfied at {self.number_of_iterations} iterations.")
        return satisfaction

    def one_step(self):
        self.number_of_iterations += 1
        self.rep = schelling.step(self.rep, threshold=self.threshold)
        ratio = self.compute_satisfaction_ratio()
        self.evolution.append(ratio)
        if self.fully_satisfied:
            self.auto_mode = False
        print(f"Step executed. Step number: {self.number_of_iterations}")

    def ten_steps(self):
        for _ in range(10):
            self.number_of_iterations += 1
            self.rep = schelling.step(self.rep, threshold=self.threshold)
            ratio = self.compute_satisfaction_ratio()
            self.evolution.append(ratio)
        print(f"10 steps executed. Step number: {self.number_of_iterations}")

    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        print("Auto mode", "enabled" if self.auto_mode else "disabled")

    def handle_events(self, events):
        for event in events:
            self.button_manager.handle_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        self.frame_count += 1
        if self.auto_mode and self.frame_count % AUTO_FPS == 0:
            self.one_step()

    def draw(self):
        self.screen.fill((255, 255, 255))
        schelling.plot(self.rep, self.screen)
        pygame.draw.rect(self.screen, (50, 50, 50), (0, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT, WINDOW_WIDTH, BOTTOM_BAR_HEIGHT))
        self.button_manager.draw(self.screen)
        self.draw_graph()

    def draw_graph(self):
        graph_rect = pygame.Rect(GRAPH_AREA_X, GRAPH_AREA_Y, GRAPH_AREA_WIDTH, GRAPH_AREA_HEIGHT)
        pygame.draw.rect(self.screen, (240, 240, 240), graph_rect)
        if len(self.evolution) < 2:
            return
        max_steps = len(self.evolution)
        x_scale = GRAPH_AREA_WIDTH / (max_steps - 1)
        points = []
        for i, ratio in enumerate(self.evolution):
            x = GRAPH_AREA_X + i * x_scale
            y = GRAPH_AREA_Y + GRAPH_AREA_HEIGHT - (ratio * GRAPH_AREA_HEIGHT)
            points.append((x, y))
        pygame.draw.lines(self.screen, (0, 0, 0), False, points, 2)
        pygame.draw.rect(self.screen, (0, 0, 0), graph_rect, 2)
