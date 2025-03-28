"""
dialogs.py

This module provides classes for displaying popup dialogs in the Snake game,
such as a Pause dialog or a Game Over dialog. Each dialog can handle its own
events and rendering.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Callable, Optional

class BaseDialog(ABC):
    """
    מחלקת בסיס עבור דיאלוגים (חלוניות הודעה).
    מגדירה ממשק לציור הדיאלוג, לטיפול באירועים ולניהול מצב סגירה.
    """
    def __init__(self,
                 screen_width: int,
                 screen_height: int,
                 font: pygame.font.Font,
                 title: str = "Dialog",
                 bg_color=(0, 0, 0, 200)) -> None:
        """
        אתחול דיאלוג בסיסי.
        
        :param screen_width: רוחב המסך (פיקסלים).
        :param screen_height: גובה המסך (פיקסלים).
        :param font: פונט עבור כותרת/טקסט.
        :param title: כותרת הדיאלוג (טקסט).
        :param bg_color: צבע רקע עם אלפא (RGBA) או ללא אלפא (RGB).
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.title = title
        self.bg_color = bg_color
        self.is_open = True  # האם הדיאלוג עדיין פתוח

        # הגדרת שטח הדיאלוג – לדוגמה מלבן באמצע המסך
        self.dialog_width = 400
        self.dialog_height = 200
        self.dialog_rect = pygame.Rect(
            (screen_width - self.dialog_width) // 2,
            (screen_height - self.dialog_height) // 2,
            self.dialog_width,
            self.dialog_height
        )

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        טיפול באירועים (כמו לחיצת מקשים/עכבר).
        מחלקות יורשות יממשו את הלוגיקה הייחודית להן.
        """
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את הדיאלוג על המסך – רקע חצי-שקוף, כותרת ו/או טקסט נוסף.
        """
        # ציור רקע חצי שקוף
        overlay = pygame.Surface((self.dialog_width, self.dialog_height), pygame.SRCALPHA)
        overlay.fill(self.bg_color)
        surface.blit(overlay, (self.dialog_rect.x, self.dialog_rect.y))

        # ציור כותרת במרכז
        title_surf = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=self.dialog_rect.center)
        surface.blit(title_surf, title_rect)


class PauseDialog(BaseDialog):
    """
    דיאלוג הפסקה (Pause).
    לדוגמה: מציג "Paused", וממתין ללחיצה על מקש מסוים (למשל 'P' או 'Escape') כדי לחזור למשחק.
    """
    def __init__(self, screen_width, screen_height, font):
        super().__init__(screen_width, screen_height, font, title="Paused", bg_color=(0, 0, 0, 180))

    def handle_event(self, event: pygame.event.Event) -> None:
        # לדוגמה: אם לוחצים על Escape או P, סוגרים את הדיאלוג
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.is_open = False


class GameOverDialog(BaseDialog):
    """
    דיאלוג סיום משחק (Game Over).
    מציג "Game Over" ומאפשר לשחקן לבחור האם לצאת או להתחיל משחק חדש.
    """
    def __init__(self, screen_width, screen_height, font,
                 on_restart: Optional[Callable[[], None]] = None):
        """
        :param on_restart: פונקציה שתופעל אם השחקן רוצה להתחיל משחק חדש.
        """
        super().__init__(screen_width, screen_height, font, title="Game Over", bg_color=(128, 0, 0, 200))
        self.on_restart = on_restart

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            # לדוגמה: R להתחלה מחדש, Escape ליציאה
            if event.key == pygame.K_r:
                if self.on_restart:
                    self.on_restart()
                self.is_open = False
            elif event.key == pygame.K_ESCAPE:
                # סוגרים דיאלוג
                self.is_open = False
