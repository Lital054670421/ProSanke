"""
hud.py

This module provides a HUD (Heads-Up Display) for the Snake game,
displaying real-time information such as score, elapsed time, game state,
and popups for newly unlocked achievements.
"""

import pygame

class HUD:
    def __init__(self, font: pygame.font.Font, screen_width: int, screen_height: int) -> None:
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.score: int = 0
        self.elapsed_time: float = 0.0
        self.game_state_text: str = ""

        self.margin = 20

        # Current popup and a queue for additional achievement popups
        self.current_popup: dict | None = None
        self.popup_timer: float = 0.0
        self.popup_queue: list[dict] = []  # New: Queue of popup messages

    def set_score(self, new_score: int) -> None:
        self.score = new_score

    def set_game_state(self, state_str: str) -> None:
        self.game_state_text = state_str

    def reset_timer(self) -> None:
        self.elapsed_time = 0.0

    def update(self, dt: float) -> None:
        """
        - Updates the game time.
        - Decrements the current popup timer and, if expired, loads the next popup from the queue.
        """
        self.elapsed_time += dt

        if self.current_popup is not None:
            self.popup_timer -= dt
            if self.popup_timer <= 0:
                # Current popup expired, move to the next in queue if available
                self.current_popup = None
                if self.popup_queue:
                    next_popup = self.popup_queue.pop(0)
                    self.current_popup = next_popup
                    self.popup_timer = next_popup["duration"]

    def add_achievement_popup(self, achievement_name: str, duration: float = 3.0) -> None:
        """
        Activates a popup for an achievement. If one is already active,
        adds the new achievement to the popup queue.
        """
        new_popup = {
            "title": "Achievement Unlocked!",
            "text": achievement_name,
            "duration": duration
        }
        if self.current_popup is None:
            self.current_popup = new_popup
            self.popup_timer = duration
        else:
            self.popup_queue.append(new_popup)

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the basic HUD (score, time, game state) and, if available,
        draws the active popup in the center of the screen.
        """
        # Draw basic HUD: score, time, game state
        score_text = f"Score: {self.score}"
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        surface.blit(score_surf, (self.margin, self.margin))

        time_text = f"Time: {int(self.elapsed_time)}s"
        time_surf = self.font.render(time_text, True, (255, 255, 255))
        surface.blit(time_surf, (self.margin, self.margin + 40))

        if self.game_state_text:
            state_surf = self.font.render(self.game_state_text, True, (255, 255, 0))
            surface.blit(state_surf, (self.margin, self.margin + 80))

        # Draw the popup if available
        if self.current_popup is not None:
            self.draw_popup(surface, self.current_popup["title"], self.current_popup["text"])

    def draw_popup(self, surface: pygame.Surface, title: str, text: str) -> None:
        """
        Draws a semi-transparent popup in the center of the screen with a title and text.
        """
        # Popup dimensions (adjust as needed)
        popup_width = 400
        popup_height = 200

        # Center position
        x = (self.screen_width - popup_width) // 2
        y = (self.screen_height - popup_height) // 2

        # Create a semi-transparent surface for the popup background
        popup_surf = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        popup_surf.fill((0, 0, 0, 160))  # Black with alpha=160

        # Draw the title (larger font)
        title_font = pygame.font.SysFont(None, 36)
        title_surf = title_font.render(title, True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(popup_width // 2, 50))
        popup_surf.blit(title_surf, title_rect)

        # Draw the achievement text
        text_font = pygame.font.SysFont(None, 28)
        text_surf = text_font.render(text, True, (255, 215, 0))
        text_rect = text_surf.get_rect(center=(popup_width // 2, 110))
        popup_surf.blit(text_surf, text_rect)

        # Blit the popup surface onto the main surface
        surface.blit(popup_surf, (x, y))
