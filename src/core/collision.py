"""
collision.py

This module provides functions for collision detection between game objects
in the Snake game. It includes functions to compare coordinates for collision
between the snake's head and the food, check collision between pygame.Rect objects,
verify if an object is outside the screen boundaries, and detect collision with obstacles.
"""

import pygame
from typing import Tuple, List

def check_collision(snake_head: Tuple[int, int], food_position: Tuple[int, int]) -> bool:
    """
    Checks if the snake's head collides with the food.
    
    בדיקה האם הקואורדינטה של ראש הנחש תואמת את מיקום האוכל.
    
    :param snake_head: A tuple (x, y) representing the snake's head position.
    :param food_position: A tuple (x, y) representing the food's position.
    :return: True if the snake's head position equals the food's position, else False.
    """
    return snake_head == food_position

def check_rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """
    Checks if two pygame.Rect objects collide.
    
    בודק אם שני מלבנים מתנגשים על ידי שימוש בפונקציה colliderect של pygame.
    
    :param rect1: The first pygame.Rect object.
    :param rect2: The second pygame.Rect object.
    :return: True if the rectangles collide, else False.
    """
    return rect1.colliderect(rect2)

def check_boundary_collision(position: Tuple[int, int], screen_width: int, screen_height: int, block_size: int) -> bool:
    """
    Checks if the given position is outside the screen boundaries.
    
    בודק אם נקודה (x, y) נמצאת מחוץ לגבולות המסך.
    
    :param position: A tuple (x, y) representing the position of the object.
    :param screen_width: The width of the screen.
    :param screen_height: The height of the screen.
    :param block_size: The size of the block (e.g., snake segment size).
    :return: True if the position is outside the boundaries, else False.
    """
    x, y = position
    if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
        return True
    return False

def check_obstacle_collision(object_rect: pygame.Rect, obstacles: List[pygame.Rect]) -> bool:
    """
    Checks if a given object (represented by a pygame.Rect) collides with any obstacle.
    
    בודק אם אובייקט מסוים (מופיע כ-pygame.Rect) מתנגש עם אחד מהמכשולים ברשימה.
    
    :param object_rect: A pygame.Rect representing the object.
    :param obstacles: A list of pygame.Rect objects representing obstacles.
    :return: True if a collision with any obstacle occurs, else False.
    """
    for obstacle in obstacles:
        if object_rect.colliderect(obstacle):
            return True
    return False
