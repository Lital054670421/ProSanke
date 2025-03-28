"""
game_logic.py

This module manages the main game loop for the Snake game.
It handles user input, updates game logic (such as snake movement, collision detection,
state transitions, and difficulty adjustments), and coordinates with the Graphics and UI modules
for rendering, animations, and visual effects.

In this version, we integrate a main menu (MainMenu) before starting the game,
and allow returning to the main menu immediately after GAME_OVER.

Changes requested:
1. Show "Game Over" on screen for a few seconds before returning to the main menu.
2. Score 50 points per apple eaten.
3. HUD shows time and score in real time.
4. Integrate SoundManager for background music and sound effects (e.g. move, food, game over).
5. Adjust game speed according to difficulty (using a discrete update via accumulator).
"""

import sys
import time
from typing import Any
import pygame
import config.settings as settings

# Importing core modules
from src.core.game_state import GameState, GameStateManager
from src.core.snake import Snake
from src.core.food import Food
from src.core.collision import check_collision
from src.core.level import LevelManager  # Includes manual difficulty setting

# Correctly import config_parser from the config folder
import config.config_parser as config_parser

# Importing graphics modules
from src.graphics.renderer import Renderer
from src.graphics.animations import AnimationManager, FadeAnimation

# Importing effects modules
from src.graphics.effects import EffectsManager, ParticleEffect

# Importing the main menu module
from src.ui.menu.main_menu import MainMenu

# --- New imports for HUD, Dialogs, and Sound ---
from src.ui.hud import HUD
from src.ui.dialogs import PauseDialog  # We won't use GameOverDialog; we'll show text ourselves.
from src.audio.sound_manager import SoundManager

class GameLogic:
    """
    מנהל את הלוגיקה המרכזית של המשחק.
    """

    def __init__(self) -> None:
        """
        מאתחל את מערכת הלוגיקה:
          - GameStateManager לניהול מצבי המשחק.
          - LevelManager לניהול רמות הקושי – ניתן לעדכן ידנית בהתאם לבחירה.
          - AnimationManager לניהול אנימציות (לדוגמה, fade in/out).
          - EffectsManager לניהול אפקטים ויזואליים (כגון חלקיקים).
          - משתנה score למעקב אחרי הניקוד.
          - HUD לתצוגה בזמן אמת.
          - SoundManager לניהול מוזיקת רקע ואפקטים קוליים.
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
        self.hud: HUD = None
        self.paused: bool = False

        # אתחול מנהל האודיו (Singleton)
        self.sound_manager = SoundManager()
        if getattr(settings, "BACKGROUND_MUSIC", True):
            self.sound_manager.play_music()

        # אפקט fade in בתחילת המשחק
        self.animation_manager.add_animation(
            FadeAnimation(
                duration=2.0,
                screen_size=(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                color=(0, 0, 0),
                fade_in=True
            )
        )

        # מאגר זמן לעדכון תנועת הנחש
        self.move_accumulator = 0.0
        self.base_interval = 0.0 # זמן בסיסי לעדכון (בשניות) לעדכון בינוני

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
                elif event.key == pygame.K_p:
                    self.handle_pause()
                # שליטה בנחש + הפעלת אפקט "SOUND_MOVE" בעת שינוי כיוון
                if self.snake:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")
                        self.sound_manager.play_sound("SOUND_MOVE")
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")
                        self.sound_manager.play_sound("SOUND_MOVE")
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")
                        self.sound_manager.play_sound("SOUND_MOVE")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")
                        self.sound_manager.play_sound("SOUND_MOVE")


    def handle_pause(self) -> None:
        """
        מפעיל דיאלוג הפסקה (PauseDialog). כל עוד הדיאלוג פתוח,
        עוצרים את עדכון המשחק ומחכים לחזרה מהדיאלוג.
        """
        self.paused = True
        pause_dialog = PauseDialog(
            screen_width=settings.SCREEN_WIDTH,
            screen_height=settings.SCREEN_HEIGHT,
            font=pygame.font.Font(settings.SNAKE_FONT_PATH, 36)
        )
        while pause_dialog.is_open:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pause_dialog.handle_event(e)
            self.render(self.screen)
            pause_dialog.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(30)
        self.paused = False

    def update(self, dt: float) -> None:
        """
        מעדכן את לוגיקת המשחק (תנועת נחש, בדיקת התנגשויות, עדכון אפקטים).
        
        :param dt: הזמן שחלף מאז העדכון הקודם (בשניות).
        """
        if self.paused:
            return
        if (self.snake is None) or (self.food is None):
            return

        if self.game_state_manager.get_state() == GameState.RUNNING:
            base_speed = settings.SNAKE_SPEED  # לדוגמה 15
            difficulty_speed = self.level_manager.strategy.get_snake_speed()
            speed_multiplier = difficulty_speed / base_speed
            move_interval = self.base_interval / speed_multiplier

            self.move_accumulator += dt
            if self.move_accumulator >= move_interval:
                self.snake.update()  # מתודת update מעדכנת את הנחש ב־block_size
                self.move_accumulator -= move_interval

            # בדיקת אכילת אוכל
            if check_collision(self.snake.body[0], self.food.position):
                self.snake.grow()
                self.food.respawn(self.snake.body)
                self.score += 50  # כל תפוח שווה 50 נקודות
                self.level_manager.update_score(self.score)
                self.effects_manager.add_effect(
                    ParticleEffect(
                        pos=self.food.position,
                        num_particles=30,
                        particle_lifetime=1.0,
                        color=(255, 255, 0),
                        particle_size=4
                    )
                )
                self.sound_manager.play_sound("SOUND_FOOD")
            
            # בדיקת התנגשות עם גבולות או עם עצמו
            if self.snake.check_self_collision() or \
               self.snake.check_wall_collision(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT):
                self.game_state_manager.set_state(GameState.GAME_OVER)
                self.sound_manager.play_sound("SOUND_GAMEOVER")

        self.animation_manager.update(dt)
        self.effects_manager.update(dt)

        if self.hud:
            self.hud.set_score(self.score)
            current_state_str = self.game_state_manager.get_state().value
            self.hud.set_game_state(current_state_str)
            self.hud.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """
        מצייר את כל רכיבי המשחק:
         - משתמש במחלקת Renderer לציור הרקע, הנחש, האוכל ומצבי המשחק.
         - מצייר אפקטים ואנימציות מעל.
         - מצייר HUD מעל הכול.
        """
        renderer = Renderer(screen)
        if self.snake and self.food:
            renderer.render_game(self.snake, self.food, self.game_state_manager.get_state())
        self.animation_manager.draw(screen)
        self.effects_manager.draw(screen)
        if self.hud:
            self.hud.draw(screen)

    def show_statistics_menu(self, screen: pygame.Surface) -> None:
        """
        מציג תפריט סטטיסטיקות שמציג את נתוני המשחק (לדוגמה, הציון הנוכחי).
        לאחר ההצגה, מחכה ללחיצה כדי לחזור לתפריט הראשי.
        """
        font = pygame.font.Font(settings.SNAKE_FONT_PATH, 36)
        header_text = "Statistics"
        score_text = f"Your Score: {self.score}"
        instruction_text = "Press any key to return to the main menu"
        running_stats = True
        while running_stats:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    running_stats = False
            screen.fill((50, 50, 50))
            header_surf = font.render(header_text, True, (255, 255, 255))
            score_surf = font.render(score_text, True, (255, 255, 255))
            instr_surf = font.render(instruction_text, True, (200, 200, 200))
            header_rect = header_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
            score_rect = score_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
            instr_rect = instr_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT * 2 // 3))
            screen.blit(header_surf, header_rect)
            screen.blit(score_surf, score_rect)
            screen.blit(instr_surf, instr_rect)
            pygame.display.flip()

    def show_game_over_text(self, screen: pygame.Surface, duration: float = 3.0) -> None:
        """
        מציג כיתוב "Game Over" על המסך למשך 'duration' שניות, ואז יוצא.
        """
        start_time = time.time()
        font = pygame.font.Font(settings.SNAKE_FONT_PATH, 48)
        while time.time() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0, 0, 0))
            text_surf = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=(settings.SCREEN_WIDTH // 2,
                                                   settings.SCREEN_HEIGHT // 2))
            screen.blit(text_surf, text_rect)
            pygame.display.flip()
            self.clock.tick(30)

    def run(self) -> None:
        """
        לולאה ראשית של התוכנית, המאפשרת לחזור לתפריט לאחר GAME_OVER.
        """
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")

        # שימוש בפונט ברירת מחדל עבור ה-HUD (System font)
        default_hud_font = pygame.font.SysFont(None, 24)
        self.hud = HUD(
            font=default_hud_font,
            screen_width=settings.SCREEN_WIDTH,
            screen_height=settings.SCREEN_HEIGHT
        )

        done = False
        while not done:
            menu = MainMenu(self.screen)
            action = menu.run()

            if action == "exit" or action is None:
                done = True

            elif action == "start":
                self.score = 0
                self.snake = Snake()
                self.food = Food()
                self.hud.reset_timer()
                # עדכון רמת הקושי לפי ההגדרות
                self.level_manager.set_difficulty(getattr(settings, "DIFFICULTY", "easy"))
                self.game_loop(self.screen)
                if self.game_state_manager.get_state() == GameState.GAME_OVER:
                    self.show_game_over_text(self.screen, duration=3.0)
                self.game_state_manager.set_state(GameState.RUNNING)

            elif action == "stats":
                self.show_statistics_menu(self.screen)

            elif action == "settings":
                from src.ui.menu.settings_menu import SettingsMenu
                settings_menu = SettingsMenu(self.screen)
                settings_menu.run()
                try:
                    updated_config = config_parser.load_config(settings.CONFIG_FILE_PATH)
                    print("Updated config loaded:", updated_config)
                except Exception as e:
                    print("Error reloading updated config:", e)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def game_loop(self, screen: pygame.Surface) -> None:
        """
        לולאת המשחק בפועל, אחרי שהמשתמש בחר 'start' בתפריט.
        """
        self.running = True
        while self.running:
            dt: float = self.clock.tick(settings.FPS) / 1000.0
            self.process_input()
            self.update(dt)
            if self.game_state_manager.get_state() == GameState.GAME_OVER:
                self.running = False
            self.render(screen)
            pygame.display.flip()
        return


if __name__ == "__main__":
    game_logic = GameLogic()
    game_logic.run()
