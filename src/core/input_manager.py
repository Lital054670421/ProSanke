# src/core/input_manager.py
import pygame
from typing import List
from src.core.snake import Snake
from src.audio.sound_manager import SoundManager
import config.settings as settings

class InputManager:
    def __init__(self, snake: Snake, sound_manager: SoundManager):
        self.snake = snake
        self.sound_manager = sound_manager

    def process_input(self) -> bool:
        """מעבד את כל אירועי הקלט ומחזיר True אם אין צורך להפסיק את הלולאה"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # סיום המשחק
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                # שאר אירועי מקלדת עבור ניהול תנועת הנחש
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
        return True
