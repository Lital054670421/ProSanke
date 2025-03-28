"""
snake.py

This module implements the Snake class which manages the snake's body,
movement, growth, self-collision detection, and now draws the snake
using images (head, body, tail) loaded from settings.py.
"""

import os
import pygame
from typing import List, Tuple

import config.settings as settings

class Snake:
    """
    מחלקת Snake מנהלת את גוף הנחש, תנועתו, הגדלתו, בדיקת התנגשות פנימית,
    וציורו באמצעות תמונות (ראש, גוף, זנב).
    הגוף מיוצג כרשימה של קואורדינטות (x, y), כאשר החלק הראשון ברשימה הוא ראש הנחש.
    """

    def __init__(self, 
                 initial_length: int = settings.INITIAL_SNAKE_LENGTH, 
                 initial_position: Tuple[int, int] = None,
                 block_size: int = settings.BLOCK_SIZE) -> None:
        """
        מאתחל את הנחש עם אורך התחלתי, מיקום התחלתי וכיוון התחלתי.
        בנוסף, טוען את כל התמונות הדרושות (head_up, head_down, וכו') מ-settings.SNAKE_IMAGES.
        
        :param initial_length: האורך ההתחלתי של הנחש (מספר חלקים).
        :param initial_position: המיקום ההתחלתי של ראש הנחש. אם לא נמסר, ממוקם במרכז המסך.
        :param block_size: גודל כל חלק (בפיקסלים).
        """
        self.block_size = block_size

        # קביעת מיקום התחלתי – אם לא נמסר, נמקם את הנחש במרכז המסך.
        if initial_position is None:
            initial_position = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)

        # כיוון התחלתי - נניח לימין
        self.direction: str = "RIGHT"

        # יצירת גוף הנחש – ראש ראשון במיקום ההתחלתי
        self.body: List[Tuple[int, int]] = [initial_position]

        # הוספת חלקים נוספים כדי להגיע לאורך ההתחלתי
        for i in range(1, initial_length):
            x, y = initial_position
            # מניחים שהנחש נע לימין, לכן החלקים הנוספים מתווספים משמאל לראש
            self.body.append((x - i * self.block_size, y))

        # טעינת התמונות מהגדרות
        self.images = {}
        for key, path in settings.SNAKE_IMAGES.items():
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (self.block_size, self.block_size))
            self.images[key] = img

    def change_direction(self, new_direction: str) -> None:
        """
        משנה את כיוון תנועת הנחש, תוך מניעת שינוי ישיר לכיוון ההפוך.
        
        :param new_direction: הכיוון החדש כ-string ("UP", "DOWN", "LEFT", "RIGHT").
        """
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction == opposites.get(self.direction):
            # אין אפשרות לעבור לכיוון ההפוך ישירות.
            return
        self.direction = new_direction

    def update(self) -> None:
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_head = (head_x, head_y - self.block_size)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + self.block_size)
        elif self.direction == "LEFT":
            new_head = (head_x - self.block_size, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + self.block_size, head_y)
        else:
            new_head = (head_x, head_y)
        
        self.body.insert(0, new_head)
        self.body.pop()


    def grow(self) -> None:
        """
        מגדיל את הנחש על ידי הוספת חלק בגוף.
        בשיטת מימוש זו, בפעם הבאה שתתבצע עדכון, הזנב לא יוסר וכך האורך יגדל.
        """
        tail = self.body[-1]
        self.body.append(tail)

    def check_self_collision(self) -> bool:
        """
        בודקת האם ראש הנחש מתנגש עם שאר חלקי הגוף.
        
        :return: True אם יש התנגשות, אחרת False.
        """
        head = self.body[0]
        return head in self.body[1:]
    
    def check_wall_collision(self, screen_width: int, screen_height: int) -> bool:
        """
        בודקת אם ראש הנחש מתנגש עם גבולות המסך.
        
        :param screen_width: רוחב המסך.
        :param screen_height: גובה המסך.
        :return: True אם יש התנגשות עם הקיר, אחרת False.
        """
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= screen_width or head_y < 0 or head_y >= screen_height:
            return True
        return False

    # פונקציות עזר לבחירת תמונות
    def get_head_image_name(self) -> str:
        """
        מחזירה את שם התמונה של הראש לפי הכיוון הנוכחי.
        """
        if self.direction == "UP":
            return "head_up"
        elif self.direction == "DOWN":
            return "head_down"
        elif self.direction == "LEFT":
            return "head_left"
        else:  # RIGHT
            return "head_right"

    def get_tail_image_name(self, tail_dir: str) -> str:
        """
        מחזירה את שם התמונה של הזנב לפי כיוון התנועה של הזנב.
        כרגע נשתמש בכיוון האחרון הידוע, או נחשב אותו.
        """
        if tail_dir == "UP":
            return "tail_up"
        elif tail_dir == "DOWN":
            return "tail_down"
        elif tail_dir == "LEFT":
            return "tail_left"
        else:  # RIGHT
            return "tail_right"

    def get_body_image_name(self, prev_pos: Tuple[int, int], curr_pos: Tuple[int, int], next_pos: Tuple[int, int]) -> str:
        """
        פונקציה בסיסית לבחירת תמונת גוף. כרגע נחזיר אופקי או אנכי, מבלי לטפל בפניות.
        אם תרצה פניות, תצטרך לנתח את כיוון התנועה (left->up, etc).
        """
        # כיוון התנועה בין prev_pos ל-curr_pos
        px, py = prev_pos
        cx, cy = curr_pos
        # כיוון התנועה בין curr_pos ל-next_pos
        nx, ny = next_pos

        # נבדוק אם מדובר בציר אופקי או אנכי
        # (אפשר כמובן להרחיב כדי לתמוך בפינות)
        if px == cx and nx == cx:
            return "body_vertical"   # אותו x => תנועה אנכית
        else:
            return "body_horizontal" # אחרת, נניח אופקי

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את הנחש על משטח התצוגה בעזרת תמונות (head, body, tail).
        """
        if not self.body:
            return

        # ---- צייר ראש ----
        head_x, head_y = self.body[0]
        head_img = self.images[self.get_head_image_name()]
        surface.blit(head_img, (head_x, head_y))

        # ---- אם יש רק חלק אחד, אין גוף ואין זנב ----
        if len(self.body) == 1:
            return

        # ---- צייר גוף (ללא זנב) ----
        for i in range(1, len(self.body) - 1):
            prev_pos = self.body[i - 1]
            curr_pos = self.body[i]
            next_pos = self.body[i + 1]
            body_img_name = self.get_body_image_name(prev_pos, curr_pos, next_pos)
            body_img = self.images[body_img_name]
            cx, cy = curr_pos
            surface.blit(body_img, (cx, cy))

        # ---- צייר זנב ----
        tail_x, tail_y = self.body[-1]
        # כדי לדעת את כיוון הזנב, נבדוק את שתי החתיכות האחרונות
        if len(self.body) >= 2:
            before_tail_x, before_tail_y = self.body[-2]
            if tail_x == before_tail_x:
                tail_dir = "UP" if tail_y < before_tail_y else "DOWN"
            else:
                tail_dir = "LEFT" if tail_x < before_tail_x else "RIGHT"
        else:
            tail_dir = "RIGHT"  # ברירת מחדל
        
        tail_img_name = self.get_tail_image_name(tail_dir)
        tail_img = self.images[tail_img_name]
        surface.blit(tail_img, (tail_x, tail_y))
