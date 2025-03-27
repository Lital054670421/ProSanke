"""
animations.py

This module handles animations for the Snake game, such as menu transitions,
game start/end effects, and special event animations. It uses a base Animation
class (using the Strategy pattern) and an AnimationManager to update and draw
active animations in synchronization with the main game loop.
"""

import pygame
from abc import ABC, abstractmethod
from typing import List, Tuple

import config.settings as settings

# -----------------------------------------------------------------------------
# Base Animation class
# -----------------------------------------------------------------------------
class Animation(ABC):
    """
    מחלקת בסיס לאנימציות.
    מגדירה את המתודות שעל כל אנימציה לממש: update() ו-draw().
    
    Abstract base class for animations. All animations must implement update() and draw().
    """
    def __init__(self, duration: float) -> None:
        """
        מאתחל את האנימציה עם משך זמן נתון.
        
        :param duration: משך האנימציה בשניות.
        """
        self.duration: float = duration
        self.elapsed: float = 0.0
        self.finished: bool = False

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        מעדכן את מצב האנימציה בהתאם לזמן החולף.
        
        :param dt: הזמן שחלף מאז העדכון הקודם (בשניות).
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את האנימציה על משטח התצוגה.
        
        :param surface: משטח התצוגה (pygame.Surface).
        """
        pass

# -----------------------------------------------------------------------------
# Concrete Fade Animation class
# -----------------------------------------------------------------------------
class FadeAnimation(Animation):
    """
    אנימציית דעיכה (Fade Animation) היוצרת אפקט מעבר חלק.
    אם fade_in=True, מתחילים עם מסך מלא בשקיפות (alpha=255) ועולים עד שקוף (alpha=0).
    אם False, מתחילים שקופים ועולים עד מלא.
    
    Fade animation that creates a smooth transition. When fade_in is True, the overlay
    starts fully opaque and fades to transparent; otherwise, it fades from transparent to opaque.
    """
    def __init__(self, duration: float, screen_size: Tuple[int, int],
                 color: Tuple[int, int, int] = (0, 0, 0), fade_in: bool = True) -> None:
        """
        אתחל את האנימציית הדעיכה.
        
        :param duration: משך האנימציה בשניות.
        :param screen_size: גודל המסך (רוחב, גובה).
        :param color: צבע העברת האנימציה (ברירת מחדל: שחור).
        :param fade_in: True אם האנימציה היא fade in, אחרת fade out.
        """
        super().__init__(duration)
        self.color: Tuple[int, int, int] = color
        self.fade_in: bool = fade_in
        self.screen_size: Tuple[int, int] = screen_size
        # הגדרת ערך התחלתי של alpha בהתאם לסוג האנימציה
        self.alpha: int = 255 if self.fade_in else 0
        # יצירת משטח overlay עם תמיכה בערוץ אלפא
        self.overlay: pygame.Surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        self.overlay.fill((*self.color, self.alpha))

    def update(self, dt: float) -> None:
        """
        מעדכן את ערך ה-alpha בהתאם להתקדמות האנימציה.
        
        :param dt: הזמן שחלף (בשניות).
        """
        self.elapsed += dt
        progress: float = min(self.elapsed / self.duration, 1.0)
        if self.fade_in:
            # מתחילים opaque (255) ועולים עד 0
            self.alpha = int(255 * (1 - progress))
        else:
            # מתחילים שקופים (0) ועולים עד opaque (255)
            self.alpha = int(255 * progress)
        # עדכון ערך האלפא במשטח
        self.overlay.fill((*self.color, self.alpha))
        if progress >= 1.0:
            self.finished = True

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את המשטח עם הערך המעודכן של alpha על המסך.
        
        :param surface: משטח התצוגה עליו יש לצייר.
        """
        surface.blit(self.overlay, (0, 0))

# -----------------------------------------------------------------------------
# Animation Manager class
# -----------------------------------------------------------------------------
class AnimationManager:
    """
    מנהל האנימציות הפעילות. אחראי לעדכן ולצייר את כל האנימציות שמתווספות אליו.
    עם עדכון כל פריים, הוא מסיר אנימציות שסיימו את פעולתן.
    
    Manages active animations by updating and drawing them each frame.
    Removes animations that have finished.
    """
    def __init__(self) -> None:
        self.animations: List[Animation] = []

    def add_animation(self, animation: Animation) -> None:
        """
        מוסיף אנימציה חדשה למערכת.
        
        :param animation: מופע של Animation.
        """
        self.animations.append(animation)

    def update(self, dt: float) -> None:
        """
        מעדכן את כל האנימציות הפעילות.
        
        :param dt: הזמן שחלף (בשניות).
        """
        for anim in self.animations[:]:
            anim.update(dt)
            if anim.finished:
                self.animations.remove(anim)

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את כל האנימציות על משטח התצוגה.
        
        :param surface: pygame.Surface שעליו יש לצייר.
        """
        for anim in self.animations:
            anim.draw(surface)

