# src/core/bomb.py
import random
import pygame
import config.settings as settings

class Bomb:
    def __init__(self, block_size: int = settings.BLOCK_SIZE, lifetime: float = 10.0) -> None:
        """
        מאתחל פצצה עם גודל בלוק וזמן חיים (למשל 10 שניות).
        """
        self.block_size = block_size
        self.lifetime = lifetime
        self.elapsed = 0.0
        self.position = (0, 0)
        # טוען את תמונת הפצצה (bomb.png) מתיקיית assets/images
        self.image = pygame.image.load("assets/images/bomb.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.block_size, self.block_size))
        # אתחל מיקום הפצצה – בהנחה שאין התנגשות עם גוף הנחש (נבדוק בעת respawn)
        self.respawn([])

    def respawn(self, snake_body: list) -> None:
        """
        בוחר מיקום אקראי לפצצה כך שהיא לא תופיע בתוך גוף הנחש.
        """
        cols = settings.SCREEN_WIDTH // self.block_size
        rows = settings.SCREEN_HEIGHT // self.block_size
        valid = False
        while not valid:
            x_cell = random.randint(0, cols - 1)
            y_cell = random.randint(0, rows - 1)
            new_pos = (x_cell * self.block_size, y_cell * self.block_size)
            if new_pos not in snake_body:
                valid = True
        self.position = new_pos
        self.elapsed = 0.0

    def update(self, dt: float) -> None:
        """
        מעדכן את הזמן שחלף עבור הפצצה.
        """
        self.elapsed += dt

    def is_expired(self) -> bool:
        """
        בודק אם זמן חיי הפצצה נגמר.
        """
        return self.elapsed >= self.lifetime

    def get_rect(self) -> pygame.Rect:
        """
        מחזיר את מלבן ההתנגשות של הפצצה.
        """
        return pygame.Rect(self.position[0], self.position[1], self.block_size, self.block_size)

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את הפצצה על המשטח.
        """
        surface.blit(self.image, self.position)
