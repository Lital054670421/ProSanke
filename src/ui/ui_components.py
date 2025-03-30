# src/ui/ui_components.py
import pygame
from typing import List, Callable

class Button:
    def __init__(self, text: str, rect: pygame.Rect, font: pygame.font.Font, on_click: Callable[[], None],
                 text_color: tuple = (255, 255, 255), bg_color: tuple = (0, 0, 0), hover_color: tuple = (50, 50, 50)):
        """
        Initializes a button with text, a rectangular area, a font, and an on_click callback.
        """
        self.text = text
        self.rect = rect
        self.font = font
        self.on_click = on_click
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the button on the given surface. Uses the hover color if the mouse is over it.
        """
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, events: List[pygame.event.Event]) -> None:
        """
        Updates the button's state based on mouse position and click events.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
                self.on_click()

class Slider:
    def __init__(self, x: int, y: int, width: int, height: int,
                 min_val: float = 0.0, max_val: float = 1.0, initial_val: float = 0.6,
                 track_color: tuple = (200, 200, 200), handle_color: tuple = (255, 0, 0)):
        """
        Initializes a slider for adjusting values (e.g., volume).
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.track_color = track_color
        self.handle_color = handle_color

        self.handle_radius = max(10, height // 2 + 4)
        self.dragging = False

    def _handle_rect(self) -> pygame.Rect:
        """
        Returns a pygame.Rect representing the handle area.
        """
        handle_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        handle_y = self.y + self.height // 2
        return pygame.Rect(handle_x - self.handle_radius,
                           handle_y - self.handle_radius,
                           self.handle_radius * 2,
                           self.handle_radius * 2)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Processes mouse events to detect handle dragging.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def update(self) -> None:
        """
        If dragging, updates the slider's value based on the mouse's x-coordinate.
        """
        if self.dragging:
            mx, _ = pygame.mouse.get_pos()
            relative_x = mx - self.x
            relative_x = max(0, min(relative_x, self.width))
            ratio = relative_x / self.width
            self.value = self.min_val + (self.max_val - self.min_val) * ratio

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the slider's track and handle.
        """
        track_rect = pygame.Rect(self.x, self.y + self.height // 2 - 2, self.width, 4)
        pygame.draw.rect(surface, self.track_color, track_rect)
        handle_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        handle_y = self.y + self.height // 2
        pygame.draw.circle(surface, self.handle_color, (handle_x, handle_y), self.handle_radius)
