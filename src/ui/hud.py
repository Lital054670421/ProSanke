"""
hud.py

This module provides a HUD (Heads-Up Display) for the Snake game,
displaying real-time information such as score, elapsed time, and game state.
"""

import pygame

class HUD:
    """
    מחלקה לייצוג תצוגת מידע בזמן אמת (Heads-Up Display).
    מציגה ניקוד, זמן משחק, מצב משחק, ועוד בהתאם לצורך.
    """
    def __init__(self, font: pygame.font.Font, screen_width: int, screen_height: int) -> None:
        """
        אתחול HUD עם פונט ומידות מסך.
        
        :param font: אובייקט pygame.font.Font לציור הטקסט.
        :param screen_width: רוחב המסך (פיקסלים).
        :param screen_height: גובה המסך (פיקסלים).
        """
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.score: int = 0
        self.elapsed_time: float = 0.0  # נצבור את הזמן בפריימים
        self.game_state_text: str = ""  # למשל "Running", "Paused", "Game Over"

        # הגדרות מיקום (ניתן לשנות לפי עיצוב)
        self.margin = 20

    def set_score(self, new_score: int) -> None:
        """
        מעדכן את ערך הניקוד המוצג ב‑HUD.
        """
        self.score = new_score

    def set_game_state(self, state_str: str) -> None:
        """
        מעדכן מחרוזת המייצגת את מצב המשחק (למשל "Running", "Paused", "Game Over").
        """
        self.game_state_text = state_str

    def reset_timer(self) -> None:
        """
        מאפס את הטיימר (למשל אם מתחילים משחק חדש).
        """
        self.elapsed_time = 0.0

    def update(self, dt: float) -> None:
        """
        עדכון נתוני ה‑HUD, למשל זמן שעבר.
        :param dt: זמן שחלף מאז העדכון הקודם (בשניות).
        """
        self.elapsed_time += dt

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את ה-HUD על המסך – ניקוד, זמן, מצב משחק.
        :param surface: משטח pygame עליו נצייר.
        """
        # ציור ניקוד
        score_text = f"Score: {self.score}"
        score_surf = self.font.render(score_text, True, (255, 255, 255))
        surface.blit(score_surf, (self.margin, self.margin))

        # ציור זמן שעבר (שניות שלמות)
        time_text = f"Time: {int(self.elapsed_time)}s"
        time_surf = self.font.render(time_text, True, (255, 255, 255))
        surface.blit(time_surf, (self.margin, self.margin + 40))

        # מצב משחק (אופציונלי)
        if self.game_state_text:
            state_surf = self.font.render(self.game_state_text, True, (255, 255, 0))
            surface.blit(state_surf, (self.margin, self.margin + 80))
