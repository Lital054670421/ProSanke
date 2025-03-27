"""
food.py

This module implements the Food class for the Snake game.
The Food class is responsible for generating a food item at a valid random position
on the screen, ensuring that the food does not appear within the snake's body.
It also provides a method to draw the food on a given pygame surface.
"""

import random
import pygame
from typing import List, Tuple

import config.settings as settings

class Food:
    """
    מחלקת Food אחראית על ניהול האוכל במשחק.
    היא מייצרת מיקום אקראי לאוכל, תוך בדיקה שהמיקום אינו בתוך גוף הנחש.
    בנוסף, היא טוענת תמונת תפוח ומציגה אותה על מסך המשחק.
    """

    def __init__(self, block_size: int = settings.BLOCK_SIZE) -> None:
        """
        מאתחל את אובייקט האוכל עם גודל בלוק נתון.
        
        :param block_size: גודל כל יחידת אוכל (בפיקסלים). ברירת מחדל: settings.BLOCK_SIZE.
        """
        self.block_size: int = block_size
        self.position: Tuple[int, int] = (0, 0)
        # טוען את תמונת התפוח מהנתיב שמוגדר ב-settings
        self.image = pygame.image.load(settings.APPLE_IMAGE_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.block_size, self.block_size))
        # אתחול מיקום האוכל; בתחילה נניח שאין גוף נחש (ניתן לעדכן בעתיד)
        self.respawn([])

    def respawn(self, snake_body: List[Tuple[int, int]]) -> None:
        """
        מגדיר מיקום חדש לאוכל כך שהמיקום לא יהיה בתוך גוף הנחש.
        משתמש במספר תאים המחושבים על פי גודל המסך וגודל הבלוק.
        
        :param snake_body: רשימת קואורדינטות (x, y) של גוף הנחש.
        """
        cols: int = settings.SCREEN_WIDTH // self.block_size
        rows: int = settings.SCREEN_HEIGHT // self.block_size

        valid_position: bool = False
        while not valid_position:
            # מגריל אינדקס תא עבור הצירים
            x_cell: int = random.randint(0, cols - 1)
            y_cell: int = random.randint(0, rows - 1)
            new_pos: Tuple[int, int] = (x_cell * self.block_size, y_cell * self.block_size)
            # בודק שהמיקום החדש אינו בתוך גוף הנחש
            if new_pos not in snake_body:
                valid_position = True

        self.position = new_pos

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את האוכל (תמונה) על משטח התצוגה.
        
        :param surface: משטח התצוגה (pygame.Surface) עליו יש לצייר את האוכל.
        """
        surface.blit(self.image, (self.position[0], self.position[1]))

# דוגמת שימוש – להרצה עצמית של הקובץ לבדיקה
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Food Test")
    clock = pygame.time.Clock()
    
    # אתחול נחש לדוגמה: רשימה לדוגמה – בדיקה ראשונית
    dummy_snake_body = [(100, 100), (80, 100), (60, 100)]
    food = Food()
    food.respawn(dummy_snake_body)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(settings.COLOR_BACKGROUND)
        food.draw(screen)
        pygame.display.flip()
        clock.tick(settings.FPS)  # FPS מוגדר ב-settings

    pygame.quit()
