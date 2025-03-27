"""
effects.py

This module adds visual effects such as particle effects and glow to enhance the user experience.
It integrates with the renderer to produce real-time effects during game events (e.g., when food is consumed).
It is designed using a modular and scalable approach, allowing easy changes and future expansions.
"""
import math
import pygame
import random
from abc import ABC, abstractmethod
from typing import List, Tuple
import config.settings as settings

# -----------------------------------------------------------------------------
# Base Effect class
# -----------------------------------------------------------------------------
class Effect(ABC):
    """
    מחלקת בסיס לאפקטים ויזואליים.
    כל אפקט חייב לממש את המתודות update() ו-draw() ולנהל את הזמן שחלף.
    """
    def __init__(self, duration: float) -> None:
        """
        אתחל את האפקט עם משך זמן מוגדר.
        
        :param duration: משך הזמן של האפקט בשניות.
        """
        self.duration: float = duration
        self.elapsed: float = 0.0
        self.finished: bool = False

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        מעדכן את מצב האפקט בהתאם לזמן החולף.
        
        :param dt: הזמן שחלף מאז העדכון הקודם (בשניות).
        """
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את האפקט על משטח התצוגה.
        
        :param surface: משטח התצוגה (pygame.Surface).
        """
        pass

# -----------------------------------------------------------------------------
# Particle class
# -----------------------------------------------------------------------------
class Particle:
    """
    מחלקת Particle מייצגת חלקיק בודד באפקט.
    כל חלקיק כולל מיקום, מהירות, זמן חיים, צבע וגודל.
    """
    def __init__(self, pos: Tuple[float, float], velocity: Tuple[float, float],
                 lifetime: float, color: Tuple[int, int, int], size: int) -> None:
        """
        אתחל את החלקיק עם המאפיינים הנתונים.
        
        :param pos: מיקום התחלתי (x, y) כ-tuples.
        :param velocity: וקטור מהירות (vx, vy).
        :param lifetime: משך זמן החיים של החלקיק בשניות.
        :param color: צבע החלקיק כ-tuples (R, G, B).
        :param size: גודל החלקיק (רדיוס במרחב).
        """
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(pos)
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(velocity)
        self.lifetime: float = lifetime
        self.color: Tuple[int, int, int] = color
        self.size: int = size
        self.age: float = 0.0

    def update(self, dt: float) -> None:
        """
        מעדכן את המיקום והגיל של החלקיק.
        
        :param dt: הזמן שחלף (בשניות).
        """
        self.pos += self.velocity * dt
        self.age += dt

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את החלקיק על המשטח, תוך חישוב שקיפותו (alpha) בהתאם לגיל.
        
        :param surface: משטח התצוגה (pygame.Surface).
        """
        # חישוב שקיפות (alpha) המבוססת על יחס הגיל לזמן החיים.
        alpha: int = max(0, 255 - int((self.age / self.lifetime) * 255))
        temp_surface: pygame.Surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, self.color + (alpha,), (self.size, self.size), self.size)
        surface.blit(temp_surface, (int(self.pos.x - self.size), int(self.pos.y - self.size)))

    def is_dead(self) -> bool:
        """
        בודק אם החלקיק עבר את זמן חייו.
        
        :return: True אם החלקיק "מת", אחרת False.
        """
        return self.age >= self.lifetime

# -----------------------------------------------------------------------------
# ParticleEffect class
# -----------------------------------------------------------------------------
class ParticleEffect(Effect):
    """
    אפקט חלקיקים שנוצר סביב נקודה מסוימת (לדוגמה, בעת צריכת אוכל).
    יוצר מספר חלקיקים באקראיות, מעדכן אותם ומצייר אותם על המסך.
    """
    def __init__(self, pos: Tuple[int, int], num_particles: int = 20,
                 particle_lifetime: float = 1.0, color: Tuple[int, int, int] = (255, 255, 0),
                 particle_size: int = 3) -> None:
        """
        אתחל את אפקט החלקיקים.
        
        :param pos: המיקום שבו ייווצרו החלקיקים.
        :param num_particles: מספר החלקיקים שייווצרו.
        :param particle_lifetime: משך חיי כל חלקיק (בשניות).
        :param color: צבע החלקיקים.
        :param particle_size: גודל כל חלקיק.
        """
        super().__init__(duration=particle_lifetime)
        self.particles: List[Particle] = []
        for _ in range(num_particles):
            # הגרלת מהירויות וכיוונים אקראיים
            angle: float = random.uniform(0, 2 * 3.14159)
            speed: float = random.uniform(50, 150)  # מהירות בין 50 ל-150 פיקסלים לשנייה
            # חישוב וקטור המהירות
            vx: float = speed * math.cos(angle)
            vy: float = speed * math.sin(angle)
            self.particles.append(
                Particle(pos=pos, velocity=(vx, vy), lifetime=particle_lifetime,
                         color=color, size=particle_size)
            )

    def update(self, dt: float) -> None:
        """
        מעדכן את כל החלקיקים, מסיר חלקיקים "מתים" ומסמן את האפקט כסתם כשהכל נגמר.
        
        :param dt: הזמן שחלף (בשניות).
        """
        self.elapsed += dt
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.is_dead():
                self.particles.remove(particle)
        if not self.particles:
            self.finished = True

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את כל החלקיקים על משטח התצוגה.
        
        :param surface: pygame.Surface שעליו יש לצייר.
        """
        for particle in self.particles:
            particle.draw(surface)

# -----------------------------------------------------------------------------
# EffectsManager class
# -----------------------------------------------------------------------------
class EffectsManager:
    """
    מנהל אפקטים ויזואליים. אחראי לעדכן ולצייר את כל האפקטים הפעילים בזמן אמת.
    """
    def __init__(self) -> None:
        self.effects: List[Effect] = []

    def add_effect(self, effect: Effect) -> None:
        """
        מוסיף אפקט חדש למערכת.
        
        :param effect: מופע של Effect.
        """
        self.effects.append(effect)

    def update(self, dt: float) -> None:
        """
        מעדכן את כל האפקטים הפעילים ומסיר את אלו שסיימו את פעולתם.
        
        :param dt: הזמן שחלף (בשניות).
        """
        for effect in self.effects[:]:
            effect.update(dt)
            if effect.finished:
                self.effects.remove(effect)

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את כל האפקטים הפעילים על משטח התצוגה.
        
        :param surface: pygame.Surface שעליו יש לצייר.
        """
        for effect in self.effects:
            effect.draw(surface)

