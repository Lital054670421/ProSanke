"""
main_menu.py

This module provides an intuitive main menu with navigation options such as
Start Game, View Statistics, Settings, and Exit. It uses a professional approach
to handle user input (mouse, keyboard), animations (if desired), and transitions
to other parts of the game.
"""

import pygame
from typing import List, Callable, Optional
import config.settings as settings

# Import the unified UI components
from src.ui.ui_components import Button

class MainMenu:
    """
    The main menu of the game. Contains buttons for main actions:
    Start Game, Statistics, Settings, Exit.
    """
    def __init__(self, screen: pygame.Surface):
        """
        Initializes the main menu with clear buttons.
        
        :param screen: The main display surface.
        """
        self.screen = screen
        # Load font from settings
        self.font = pygame.font.Font(settings.SNAKE_FONT_PATH, 36)

        # List of buttons
        self.buttons: List[Button] = []

        # Assume the center of the screen is:
        center_x = settings.SCREEN_WIDTH // 2
        center_y = settings.SCREEN_HEIGHT // 2

        # Button dimensions
        btn_width, btn_height = 200, 60
        gap = 80  # Vertical gap between buttons

        # Create buttons
        # Start Game
        self.buttons.append(Button(
            text="Start Game",
            rect=pygame.Rect(center_x - btn_width // 2, center_y - gap, btn_width, btn_height),
            font=self.font,
            on_click=self.start_game,
            text_color=(255, 255, 255),
            bg_color=(0, 100, 0),
            hover_color=(0, 150, 0)
        ))

        # Statistics
        self.buttons.append(Button(
            text="Statistics",
            rect=pygame.Rect(center_x - btn_width // 2, center_y, btn_width, btn_height),
            font=self.font,
            on_click=self.view_statistics,
            text_color=(255, 255, 255),
            bg_color=(0, 100, 100),
            hover_color=(0, 150, 150)
        ))

        # Settings
        self.buttons.append(Button(
            text="Settings",
            rect=pygame.Rect(center_x - btn_width // 2, center_y + gap, btn_width, btn_height),
            font=self.font,
            on_click=self.view_settings,
            text_color=(255, 255, 255),
            bg_color=(100, 0, 100),
            hover_color=(150, 0, 150)
        ))

        # Exit
        self.buttons.append(Button(
            text="Exit",
            rect=pygame.Rect(center_x - btn_width // 2, center_y + 2 * gap, btn_width, btn_height),
            font=self.font,
            on_click=self.exit_game,
            text_color=(255, 255, 255),
            bg_color=(100, 0, 0),
            hover_color=(150, 0, 0)
        ))

        self.running = True
        self.next_action = None  # Can be "start", "stats", "settings", "exit"

    def start_game(self):
        print("Start Game clicked!")
        self.next_action = "start"
        self.running = False

    def view_statistics(self):
        print("Statistics clicked!")
        self.next_action = "stats"
        self.running = False

    def view_settings(self):
        print("Settings clicked!")
        self.next_action = "settings"
        self.running = False

    def exit_game(self):
        print("Exit clicked!")
        self.next_action = "exit"
        self.running = False

    def run(self) -> str:
        """
        Displays the main menu in a loop until the user selects an action.
        
        :return: A string indicating the next action (e.g., "start", "stats", "settings", "exit").
        """
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(settings.FPS) / 1000.0

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.next_action = "exit"
                    self.running = False

            # Update buttons state
            for btn in self.buttons:
                btn.update(events)

            # Draw background and buttons
            self.screen.fill((30, 30, 30))  # Dark gray background
            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()

        # Return the action selected by the user
        return self.next_action
