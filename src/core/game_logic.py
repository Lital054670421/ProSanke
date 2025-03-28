"""
game_logic.py

This module manages the main game loop for the Snake game.
It handles user input, updates game logic (such as snake movement, collision detection,
state transitions, and difficulty adjustments), and coordinates with the Graphics and UI modules
for rendering, animations, and visual effects.

Changes implemented:
1. Show "Game Over" on screen for a few seconds before returning to the main menu.
2. Score 50 points per apple eaten.
3. HUD shows time and score in real time.
4. Integrate SoundManager for background music and sound effects.
5. Adjust game speed according to difficulty using a discrete update via accumulator.
6. Integrate StatsManager to update and save game statistics after each game.
7. Display a popup message when a new achievement is unlocked (NEW).
8. Achievement popups are now fully managed by the HUD (instead of game_logic).
"""

import sys
import time
from typing import Any
import pygame
import config.settings as settings

# Core modules
from src.core.game_state import GameState, GameStateManager
from src.core.snake import Snake
from src.core.food import Food
from src.core.collision import check_collision
from src.core.level import LevelManager  # Includes manual difficulty setting

import config.config_parser as config_parser

# Graphics
from src.graphics.renderer import Renderer
from src.graphics.animations import AnimationManager, FadeAnimation

# Effects
from src.graphics.effects import EffectsManager, ParticleEffect

# Menu
from src.ui.menu.main_menu import MainMenu

# HUD, Dialogs, Sound
from src.ui.hud import HUD
from src.ui.dialogs import PauseDialog
from src.audio.sound_manager import SoundManager

# StatsManager integration
from src.stats.stats_manager import StatsManager


class GameLogic:
    def __init__(self) -> None:
        self.game_state_manager: GameStateManager = GameStateManager(initial_state=GameState.RUNNING)
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.snake: Snake = None
        self.food: Food = None
        self.running: bool = True
        self.score: int = 0

        # Difficulty Level Manager
        self.level_manager: LevelManager = LevelManager(initial_score=self.score)

        # Animation & Effects
        self.animation_manager: AnimationManager = AnimationManager()
        self.effects_manager: EffectsManager = EffectsManager()

        # HUD (Heads-Up Display)
        self.hud: HUD = None
        self.paused: bool = False

        # SoundManager (Singleton)
        self.sound_manager = SoundManager()
        if getattr(settings, "BACKGROUND_MUSIC", True):
            self.sound_manager.play_music()

        # Fade-in animation at game start
        self.animation_manager.add_animation(
            FadeAnimation(
                duration=2.0,
                screen_size=(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
                color=(0, 0, 0),
                fade_in=True
            )
        )

        # Accumulator for discrete movement
        self.move_accumulator = 0.0
        self.base_interval = 0.15  # base for "medium" difficulty

        # StatsManager with a callback that will add a popup to the HUD
        self.stats_manager = StatsManager(
            username="Player",
            achievement_callback=self.on_achievement_unlocked
        )

    def on_achievement_unlocked(self, achievement: str) -> None:
        """
        Called when StatsManager unlocks a new achievement.
        We delegate the popup display to the HUD, which manages achievement popups.
        """
        print(f"[Achievement Notification] Unlocked: {achievement}")
        if self.hud:
            # HUD now manages the popups:
            self.hud.add_achievement_popup(achievement_name=achievement, duration=5.0)

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.handle_pause()

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
        Opens a pause dialog. While paused, game logic updates are stopped.
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
        Main update logic for the game loop:
        - If paused, do nothing.
        - If running, move the snake discretely based on difficulty.
        - Check collisions, play sounds, update animations & HUD.
        """
        if self.paused:
            return
        if not (self.snake and self.food):
            return

        if self.game_state_manager.get_state() == GameState.RUNNING:
            base_speed = settings.SNAKE_SPEED
            difficulty_speed = self.level_manager.strategy.get_snake_speed()
            speed_multiplier = difficulty_speed / base_speed

            move_interval = self.base_interval / speed_multiplier
            self.move_accumulator += dt
            if self.move_accumulator >= move_interval:
                self.snake.update()
                self.move_accumulator -= move_interval

            # Check if snake ate food
            if check_collision(self.snake.body[0], self.food.position):
                self.snake.grow()
                self.food.respawn(self.snake.body)
                self.score += 50
                self.level_manager.update_score(self.score)
                # Particle effect & sound
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

            # Check if snake hit wall or itself
            if self.snake.check_self_collision() or \
               self.snake.check_wall_collision(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT):
                self.game_state_manager.set_state(GameState.GAME_OVER)
                self.sound_manager.play_sound("SOUND_GAMEOVER")

        # Update animations & effects
        self.animation_manager.update(dt)
        self.effects_manager.update(dt)

        # Update HUD
        if self.hud:
            self.hud.set_score(self.score)
            current_state_str = self.game_state_manager.get_state().value
            self.hud.set_game_state(current_state_str)
            self.hud.update(dt)

    def render(self, screen: pygame.Surface) -> None:
        """
        Renders all game objects (snake, food), plus animations, effects, and HUD.
        """
        renderer = Renderer(screen)

        if self.snake and self.food:
            renderer.render_game(self.snake, self.food, self.game_state_manager.get_state())

        self.animation_manager.draw(screen)
        self.effects_manager.draw(screen)

        # Finally draw the HUD
        if self.hud:
            self.hud.draw(screen)

    def show_statistics_menu(self, screen: pygame.Surface) -> None:
        """
        Shows a simple statistics menu using the stats_manager data.
        """
        font = pygame.font.Font(settings.SNAKE_FONT_PATH, 36)
        highest_score = self.stats_manager.get_highest_score()
        total_games = self.stats_manager.get_total_games()
        total_time = self.stats_manager.get_total_time_played()
        achievements = self.stats_manager.get_achievements()

        running_stats = True
        while running_stats:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    running_stats = False

            screen.fill((50, 50, 50))

            title_surf = font.render("Statistics", True, (255, 255, 255))
            screen.blit(title_surf, title_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 50)))

            hs_surf = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
            screen.blit(hs_surf, (50, 120))

            tg_surf = font.render(f"Total Games: {total_games}", True, (255, 255, 255))
            screen.blit(tg_surf, (50, 170))

            tt_surf = font.render(f"Total Time Played: {int(total_time)}s", True, (255, 255, 255))
            screen.blit(tt_surf, (50, 220))

            y_offset = 270
            ach_title = font.render("Achievements:", True, (255, 255, 255))
            screen.blit(ach_title, (50, y_offset))
            y_offset += 40
            for ach in achievements:
                ach_surf = font.render(f"- {ach}", True, (200, 200, 200))
                screen.blit(ach_surf, (70, y_offset))
                y_offset += 40

            pygame.display.flip()

    def show_game_over_text(self, screen: pygame.Surface, duration: float = 3.0) -> None:
        """
        Shows a 'GAME OVER' text on the screen for a fixed duration.
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
        The main program loop that keeps returning to the MainMenu until 'exit' is chosen.
        """
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")

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

                # Load difficulty from config
                try:
                    config_data = config_parser.load_config(settings.CONFIG_FILE_PATH)
                    difficulty = config_data.get("DIFFICULTY", "easy")
                except Exception as e:
                    print("Error loading difficulty from config:", e)
                    difficulty = "easy"
                self.level_manager.set_difficulty(difficulty)

                start_time = time.time()
                self.game_loop(self.screen)
                play_time = time.time() - start_time

                if self.game_state_manager.get_state() == GameState.GAME_OVER:
                    self.show_game_over_text(self.screen, duration=3.0)
                    self.stats_manager.update_game_result(self.score, play_time, player_name="Player")

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
        A single 'play' session after the user chooses 'start' from the main menu.
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
