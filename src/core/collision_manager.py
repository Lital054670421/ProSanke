# src/core/collision_manager.py
from src.core.collision import check_collision
from src.core.snake import Snake
from src.core.food import Food
from src.core.bomb_manager import BombManager
import config.settings as settings

class CollisionManager:
    def __init__(self, snake: Snake, food: Food, bomb_manager: BombManager = None):
        self.snake = snake
        self.food = food
        self.bomb_manager = bomb_manager

    def check_food_collision(self) -> bool:
        """בודק אם ראש הנחש מתנגש עם האוכל"""
        return check_collision(self.snake.body[0], self.food.position)

    def check_bomb_collision(self) -> tuple[bool, any]:
        """
        בודק אם ראש הנחש מתנגש עם פצצה.
        מחזיר (True, bomb) במקרה של התנגשות, אחרת (False, None)
        """
        if self.bomb_manager:
            for bomb in self.bomb_manager.bombs:
                if self.snake.body[0] == bomb.position:
                    return True, bomb
        return False, None

    def check_wall_or_self_collision(self) -> bool:
        """בודק אם הנחש מתנגש עם עצמו או עם גבולות המסך"""
        return self.snake.check_self_collision() or \
               self.snake.check_wall_collision(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
