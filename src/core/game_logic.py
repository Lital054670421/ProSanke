"""
game_logic.py

This module manages the main game loop for the Snake game.
It handles user input, updates game logic (such as snake movement, collision detection,
state transitions, and difficulty adjustments), and coordinates with the Graphics and UI modules
for rendering, animations, and visual effects.
"""

import sys
from typing import Any
import pygame
import config.settings as settings

# Importing core modules (using absolute imports for consistency)
from src.core.game_state import GameState, GameStateManager
from src.core.snake import Snake
from src.core.food import Food
from src.core.collision import check_collision
from src.core.level import LevelManager

# Importing graphics modules
from src.graphics.renderer import Renderer
from src.graphics.animations import AnimationManager, FadeAnimation

# Importing effects modules
from src.graphics.effects import EffectsManager, ParticleEffect

# Uncomment the following line if integrating audio functionality:
# from src.audio.sound_manager import SoundManager

class GameLogic:
    """
    מנהל את הלוגיקה המרכזית של המשחק.
    אחראי על טיפול בקלט, עדכון לוגיקת המשחק (תנועת נחש, התנגשויות, עדכון רמות קושי)
    וכן תיאום עם מודולי הגרפיקה, האנימציות והאפקטים לציור בזמן אמת.
    """

    def __init__(self) -> None:
        """
        מאתחל את מערכת הלוגיקה:
          - GameStateManager לניהול מצבי המשחק.
          - LevelManager לניהול רמות הקושי בהתאם לציון.
          - AnimationManager לניהול אנימציות (לדוגמה, fade in/out).
          - EffectsManager לניהול אפקטים ויזואליים (כגון חלקיקים).
          - משתנה score למעקב אחרי הציון.
          - (אין אתחול של Snake ו-Food כאן, כדי שהטעינה של התמונות תתבצע לאחר אתחול המסך)
        """
        self.game_state_manager: GameStateManager = GameStateManager(initial_state=GameState.RUNNING)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.snake: Snake = None  # יאוכלס בתוך run() לאחר אתחול Pygame
        self.food: Food = None    # יאוכלס בתוך run() לאחר אתחול Pygame
        self.running: bool = True
        self.score: int = 0
        self.level_manager: LevelManager = LevelManager(initial_score=self.score)
        self.animation_manager: AnimationManager = AnimationManager()
        self.effects_manager: EffectsManager = EffectsManager()
        # ניתן להוסיף אפקט fade in בתחילת המשחק:
        self.animation_manager.add_animation(
            FadeAnimation(duration=2.0,
                          screen_size=(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                          color=(0, 0, 0), fade_in=True)
        )
        # לדוגמה: self.sound_manager = SoundManager.get_instance()

    def process_input(self) -> None:
        """
        מעבד את קלט המשתמש (אירועים, מקשי חיצים) ומעדכן את כיוון הנחש.
        במידה והמשתמש סוגר את החלון או לוחץ Escape, סוגר את המשחק.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")

    def update(self, dt: float) -> None:
        """
        מעדכן את הלוגיקה של המשחק:
          - מעדכן את תנועת הנחש.
          - בודק התנגשויות בין ראש הנחש לאוכל.
          - אם הנחש אוכל, מגדיל את הנחש, מחדש את האוכל, מעדכן את הציון,
            ומעדכן את רמת הקושי.
          - בודק התנגשויות בין הנחש לגבולות או לעצמו, ומעדכן את מצב המשחק.
          - מעדכן את האנימציות והאפקטים.
        
        :param dt: הזמן שחלף מאז העדכון הקודם (בשניות).
        """
        if self.game_state_manager.get_state() == GameState.RUNNING:
            self.snake.update(dt)
            # בדיקה האם ראש הנחש מתנגש עם האוכל
            if check_collision(self.snake.body[0], self.food.position):
                self.snake.grow()  # מגדיל את הנחש
                self.food.respawn(self.snake.body)  # מגריל מיקום חדש לאוכל תוך בדיקת גוף הנחש
                self.score += 10
                self.level_manager.update_score(self.score)
                # הוספת אפקט חלקיקים בעת צריכת אוכל
                self.effects_manager.add_effect(
                    ParticleEffect(pos=self.food.position, num_particles=30,
                                   particle_lifetime=1.0, color=(255, 255, 0), particle_size=4)
                )
                # לדוגמה: self.sound_manager.play_food_sound()
            
            # בדיקה אם הנחש מתנגש בעצמו או עם גבולות המסך
            if self.snake.check_self_collision() or self.snake.check_wall_collision(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT):
                self.game_state_manager.set_state(GameState.GAME_OVER)
                # לדוגמה: self.sound_manager.play_gameover_sound()
        
        # עדכון אנימציות ואפקטים (גם במצבים שאינם פעילים)
        self.animation_manager.update(dt)
        self.effects_manager.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """
        מצייר את כל רכיבי המשחק:
          - מטעין את הרקע, הנחש, האוכל, והודעות על בסיס מצב המשחק.
          - מצייר גם את האנימציות והאפקטים שמנוהלים על ידי המערכות המתאימות.
        
        :param screen: משטח התצוגה (pygame.Surface) עליו יש לצייר.
        """
        # פונקציית render_game ממודול renderer תעשה את הציור הבסיסי
        from src.graphics.renderer import render_game
        render_game(screen, self.snake, self.food, self.game_state_manager.get_state())
        # ציור אנימציות ואפקטים
        self.animation_manager.draw(screen)
        self.effects_manager.draw(screen)

    def run(self) -> None:
        """
        הלולאה המרכזית של המשחק:
          - אתחל את Pygame, את המסך, ואת Renderer.
          - אתחל את אובייקטי המשחק (Snake, Food) אחרי אתחול המסך כדי שהטעינה של התמונות תעבוד.
          - בכל פריים: מעבד קלט, מעדכן לוגיקה, מצייר את המסך, ומעדכן את האנימציות והאפקטים.
          - סוגר את המשחק כאשר המשתמש בוחר.
        """
        pygame.init()
        screen: pygame.Surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        
        # אתחול Renderer (שמטפל ברקע ובציור האובייקטים)
        from src.graphics.renderer import Renderer
        renderer = Renderer(screen)
        
        # עכשיו, אחרי אתחול המסך, אתחל את אובייקטי המשחק:
        self.snake = Snake()  # כעת, טעינת התמונות במחלקת Snake תצליח
        self.food = Food()
        
        while self.running:
            dt: float = self.clock.tick(settings.FPS) / 1000.0
            self.process_input()
            self.update(dt)
            
            # ציור בסיסי דרך ה-Renderer
            renderer.render_game(self.snake, self.food, self.game_state_manager.get_state())
            # ציור אנימציות ואפקטים מעל המסך
            self.animation_manager.draw(screen)
            self.effects_manager.draw(screen)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

# דוגמת שימוש: הרצת המשחק כמודול עצמאי
if __name__ == "__main__":
    game_logic = GameLogic()
    game_logic.run()
