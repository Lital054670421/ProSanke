# src/core/bomb_manager.py
import pygame
import config.settings as settings
from src.core.bomb import Bomb

class BombManager:
    def __init__(self, spawn_interval: float = 5.0, bomb_lifetime: float = 10.0) -> None:
        """
        מנהל פצצות.
        :param spawn_interval: מרווח זמן (בשניות) בין ספאונים.
        :param bomb_lifetime: זמן חיים של כל פצצה (בשניות).
        """
        self.spawn_interval = spawn_interval
        self.bomb_lifetime = bomb_lifetime
        self.spawn_timer = 0.0
        self.bombs = []  # רשימת מופעי Bomb

    def update(self, dt: float, snake_body: list) -> None:
        """
        מעדכן את הזמן, יוצר פצצות חדשות בעת הצורך ומעדכן כל פצצה.
        :param dt: זמן שחלף.
        :param snake_body: גוף הנחש, כדי למנוע ספאון בתוך הנחש.
        """
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            new_bomb = Bomb(block_size=settings.BLOCK_SIZE, lifetime=self.bomb_lifetime)
            new_bomb.respawn(snake_body)
            self.bombs.append(new_bomb)
            self.spawn_timer -= self.spawn_interval

        # עדכון כל פצצה ובדיקה אם זמן חייה נגמר
        for bomb in self.bombs[:]:
            bomb.update(dt)
            if bomb.is_expired():
                self.bombs.remove(bomb)

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את כל הפצצות על המסך.
        """
        for bomb in self.bombs:
            bomb.draw(surface)
