"""
renderer.py

This module handles the rendering of game elements onto the display using Pygame.
It loads and draws a background image (if available), draws game objects (such as the snake and food),
and displays overlay messages based on the current game state (e.g., paused, game over).
"""

import pygame
from typing import Optional
import config.settings as settings
from ..core.snake import Snake
from ..core.food import Food
from ..core.game_state import GameState

class Renderer:
    """
    מחלקת Renderer אחראית על ציור המסך ועדכון כל רכיבי המשחק.
    היא טוענת את תמונת הרקע (אם זמינה) ומציגה את האובייקטים באמצעות Pygame.
    """
    
    def __init__(self, screen: pygame.Surface) -> None:
        """
        אתחל את Renderer עם משטח התצוגה, טען את הרקע (אם קיים) והגדר את הפונט לשימוש בהודעות.
        
        :param screen: משטח התצוגה (pygame.Surface) עליו יוצגו כל האלמנטים.
        """
        self.screen: pygame.Surface = screen
        self.background: Optional[pygame.Surface] = None
        self.load_background()
        # טוען את הפונט מהנתיב המוגדר ב-settings עם גודל 36 (ניתן להתאים לפי הצורך)
        self.font: pygame.font.Font = pygame.font.Font(settings.SNAKE_FONT_PATH, 36)
        
    def render_background_tiled(self) -> None:
        """
        מצייר רקע באמצעות אריח (tile) שחוזר על עצמו על פני כל המסך.
        """
        tile_img = pygame.image.load("assets/images/block1.jpg").convert()
        tile_img = pygame.transform.scale(tile_img, (settings.BLOCK_SIZE, settings.BLOCK_SIZE))
        
        # לדוגמה, נשתמש בתבנית שחמטית: נסיר את התנאי אם רוצים רק את block1, אבל כאן נעשה דוגמה לשילוב block1 ו-block2
        tile_img2 = pygame.image.load("assets/images/block2.jpg").convert()
        tile_img2 = pygame.transform.scale(tile_img2, (settings.BLOCK_SIZE, settings.BLOCK_SIZE))
        
        for x in range(0, settings.SCREEN_WIDTH, settings.BLOCK_SIZE):
            for y in range(0, settings.SCREEN_HEIGHT, settings.BLOCK_SIZE):
                if ((x // settings.BLOCK_SIZE) + (y // settings.BLOCK_SIZE)) % 2 == 0:
                    self.screen.blit(tile_img, (x, y))
                else:
                    self.screen.blit(tile_img2, (x, y))


    def load_background(self) -> None:
        """
        טוען את תמונת הרקע מהנתיב המוגדר ב-settings.
        במידה והטעינה נכשלה, המערכת תשתמש בצבע רקע סטנדרטי.
        """
        try:
            bg_image: pygame.Surface = pygame.image.load(settings.BACKGROUND_IMAGE_PATH)
            # שינוי גודל התמונה לגודל המסך להבטחת כיסוי מלא
            self.background = pygame.transform.scale(bg_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        except Exception as e:
            print("Error loading background image:", e)
            self.background = None

    def render_game(self, snake: Snake, food: Food, game_state: GameState) -> None:
        """
        מצייר את כל רכיבי המשחק בהתאם למצב הנוכחי.
        - אם יש תמונת רקע נטענת, היא תוצג. אחרת, ימולא המסך בצבע רקע מ־settings.
        - האוכל והנחש מצוירים באמצעות המתודות שלהם.
        - במידה והמשחק לא במצב RUNNING, מוצגת הודעה מרכזית (Paused או Game Over).
        
        :param snake: מופע מחלקת Snake.
        :param food: מופע מחלקת Food.
        :param game_state: המצב הנוכחי של המשחק (GameState).
        """
        # ציור הרקע: אם קיימת תמונת רקע, נשתמש בה, אחרת נמלא בצבע רקע.
        self.render_background_tiled()
        
        # ציור האובייקטים: אוכל ונחש.
        food.draw(self.screen)
        snake.draw(self.screen)
        
        # במידה והמשחק אינו במצב RUNNING, מציגים הודעת מצב במרכז המסך.
        if game_state != GameState.RUNNING:
            overlay_text: str = ""
            if game_state == GameState.PAUSED:
                overlay_text = "Paused"
            elif game_state == GameState.GAME_OVER:
                overlay_text = "Game Over"
            
            if overlay_text:
                text_surface: pygame.Surface = self.font.render(overlay_text, True, (255, 255, 255))
                # מרכז את הטקסט במסך
                text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
                self.screen.blit(text_surface, text_rect)
