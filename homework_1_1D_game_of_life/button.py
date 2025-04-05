# button.py

import pygame

class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.hover = False
        self.font = pygame.font.SysFont("Arial", 20)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, surface):
        shadow_offset = (3, 3)
        shadow_rect = self.rect.copy()
        shadow_rect.x += shadow_offset[0]
        shadow_rect.y += shadow_offset[1]
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect, border_radius=5)

        button_color = (70, 130, 180)
        if self.hover:
            button_color = (100, 149, 237)
        pygame.draw.rect(surface, button_color, self.rect, border_radius=5)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        surface.blit(self.text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()

class ButtonManager:
    def __init__(self, window_width, window_height, bottom_bar_height):
        self.buttons = {}
        button_width = 150
        button_height = 40
        margin = 20
        y = window_height - bottom_bar_height / 2 - button_height / 2
        x1 = margin
        x2 = window_width - button_width - margin

        self.buttons["one"] = Button((x1, y, button_width, button_height), "1 Generation", None)
        self.buttons["fifty"] = Button((x2, y, button_width, button_height), "50 Generations", None)

    def set_callback(self, name, callback):
        if name in self.buttons:
            self.buttons[name].callback = callback

    def handle_event(self, event):
        for button in self.buttons.values():
            button.handle_event(event)

    def draw(self, surface):
        for button in self.buttons.values():
            button.draw(surface)
