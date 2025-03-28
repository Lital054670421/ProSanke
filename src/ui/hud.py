"""
hud.py

This module provides a HUD (Heads-Up Display) for the Snake game,
displaying real-time information such as score, elapsed time, game state,
and popups for newly unlocked achievements.
"""

import pygame

# hud.py

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

        # הכנה לפופאפ יחיד
        self.current_popup: dict | None = None
        self.popup_timer: float = 0.0

    def set_score(self, new_score: int) -> None:
        self.score = new_score

    def set_game_state(self, state_str: str) -> None:
        self.game_state_text = state_str

    def reset_timer(self) -> None:
        self.elapsed_time = 0.0

    def update(self, dt: float) -> None:
        """
        - מעדכן את זמן המשחק
        - מוריד את הטיימר של הפופאפ (אם יש)
        """
        self.elapsed_time += dt

        if self.current_popup is not None:
            self.popup_timer -= dt
            if self.popup_timer <= 0:
                self.current_popup = None  # מסירים את הפופאפ

    def add_achievement_popup(self, achievement_name: str, duration: float = 3.0) -> None:
        """
        מפעיל "חלון" מרכזי לחגיגת הישג – רק אחד בכל פעם.
        אם כבר יש פופאפ פעיל, אפשר להחליט להחליף אותו או להתעלם, לבחירתך.
        כאן נחליף אותו בפופאפ החדש.
        """
        self.current_popup = {
            "title": f"Achievement Unlocked!",
            "text": f"{achievement_name}"
        }
        self.popup_timer = duration

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר ניקוד, זמן, מצב משחק + מצייר (אם יש) את ה-popup במרכז המסך.
        """
        # --- ציור HUD בסיסי (ניקוד, זמן, מצב) ---
        score_text = f"Score: {self.score}"
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        surface.blit(score_surf, (self.margin, self.margin))

        time_text = f"Time: {int(self.elapsed_time)}s"
        time_surf = self.font.render(time_text, True, (255, 255, 255))
        surface.blit(time_surf, (self.margin, self.margin + 40))

        if self.game_state_text:
            state_surf = self.font.render(self.game_state_text, True, (255, 255, 0))
            surface.blit(state_surf, (self.margin, self.margin + 80))

        # --- ציור הפופאפ אם הוא קיים ---
        if self.current_popup is not None:
            self.draw_popup(surface, self.current_popup["title"], self.current_popup["text"])

    def draw_popup(self, surface: pygame.Surface, title: str, text: str) -> None:
        """
        מצייר מלבן חצי־שקוף במרכז המסך, עם כותרת וטקסט ההישג.
        """
        # מידות החלון (תתאים כרצונך)
        popup_width = 400
        popup_height = 200

        # מיקום (מרכז המסך)
        x = (self.screen_width - popup_width) // 2
        y = (self.screen_height - popup_height) // 2

        # הכנת משטח חצי־שקוף לציור הרקע
        popup_surf = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
        # צבע רקע: שחור עם אלפא 160 (מתוך 255)
        popup_surf.fill((0, 0, 0, 160))

        # צייר כותרת – גדול יחסית
        title_font = pygame.font.SysFont(None, 36)
        title_surf = title_font.render(title, True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(popup_width // 2, 50))
        popup_surf.blit(title_surf, title_rect)

        # צייר טקסט ההישג
        text_font = pygame.font.SysFont(None, 28)
        text_surf = text_font.render(text, True, (255, 215, 0))
        text_rect = text_surf.get_rect(center=(popup_width // 2, 110))
        popup_surf.blit(text_surf, text_rect)

        # לבסוף שופך את המשטח על המסך
        surface.blit(popup_surf, (x, y))
