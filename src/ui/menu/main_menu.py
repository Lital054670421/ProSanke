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

class Button:
    """
    כפתור פשוט המוצג על המסך, הכולל טקסט, מלבן לחיצה ופונקציית פעולה.
    """
    def __init__(self, text: str, x: int, y: int, width: int, height: int,
                 font: pygame.font.Font,
                 on_click: Callable[[], None],
                 text_color=(255, 255, 255),
                 bg_color=(0, 0, 0),
                 hover_color=(50, 50, 50)):
        """
        מאתחל כפתור עם טקסט, מיקום ומידות, פונטים וצבעים.
        
        :param text: הטקסט שמופיע בכפתור.
        :param x: מיקום X על המסך של הכפתור.
        :param y: מיקום Y על המסך של הכפתור.
        :param width: רוחב הכפתור.
        :param height: גובה הכפתור.
        :param font: אובייקט pygame.font.Font לציור הטקסט.
        :param on_click: פונקציה שתתבצע כאשר לוחצים על הכפתור.
        :param text_color: צבע הטקסט.
        :param bg_color: צבע רקע הכפתור במצב רגיל.
        :param hover_color: צבע רקע הכפתור במצב ריחוף (hover).
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.on_click = on_click
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את הכפתור על המסך.
        אם העכבר מרחף, נצבע את הרקע בצבע hover, אחרת בצבע רגיל.
        """
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)

        # ציור הטקסט במרכז הכפתור
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, events: List[pygame.event.Event]) -> None:
        """
        מעדכן את מצב הכפתור (האם העכבר מרחף מעל?) ובודק לחיצה.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.is_hovered:
                    # לחיצה שמאלית על הכפתור
                    self.on_click()

class MainMenu:
    """
    התפריט הראשי של המשחק. מכיל כפתורים לפעולות עיקריות:
    Start Game, Statistics, Settings, Exit.
    """
    def __init__(self, screen: pygame.Surface):
        """
        אתחול התפריט הראשי עם כפתורים ברורים.
        
        :param screen: משטח התצוגה העיקרי (pygame.Surface).
        """
        self.screen = screen
        # ניתן לטעון פונט מהנתיב שמוגדר ב-settings
        self.font = pygame.font.Font(settings.SNAKE_FONT_PATH, 36)

        # רשימת כפתורים
        self.buttons: List[Button] = []

        # נניח שמרכז המסך הוא:
        center_x = settings.SCREEN_WIDTH // 2
        center_y = settings.SCREEN_HEIGHT // 2

        # רוחב וגובה כפתור לדוגמה
        btn_width, btn_height = 200, 60
        gap = 80  # מרחק אנכי בין כפתור לכפתור

        # יצירת כפתורים לדוגמה
        # Start Game
        self.buttons.append(Button(
            text="Start Game",
            x=center_x - btn_width//2,
            y=center_y - gap,
            width=btn_width,
            height=btn_height,
            font=self.font,
            on_click=self.start_game,
            text_color=(255, 255, 255),
            bg_color=(0, 100, 0),
            hover_color=(0, 150, 0)
        ))

        # Statistics
        self.buttons.append(Button(
            text="Statistics",
            x=center_x - btn_width//2,
            y=center_y,
            width=btn_width,
            height=btn_height,
            font=self.font,
            on_click=self.view_statistics,
            text_color=(255, 255, 255),
            bg_color=(0, 100, 100),
            hover_color=(0, 150, 150)
        ))

        # Settings
        self.buttons.append(Button(
            text="Settings",
            x=center_x - btn_width//2,
            y=center_y + gap,
            width=btn_width,
            height=btn_height,
            font=self.font,
            on_click=self.view_settings,
            text_color=(255, 255, 255),
            bg_color=(100, 0, 100),
            hover_color=(150, 0, 150)
        ))

        # Exit
        self.buttons.append(Button(
            text="Exit",
            x=center_x - btn_width//2,
            y=center_y + 2*gap,
            width=btn_width,
            height=btn_height,
            font=self.font,
            on_click=self.exit_game,
            text_color=(255, 255, 255),
            bg_color=(100, 0, 0),
            hover_color=(150, 0, 0)
        ))

        self.running = True
        self.next_action = None  # יכול להיות "start", "stats", "settings", "exit"

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
        מציג את התפריט הראשי בלולאה עד שמשתמש בוחר פעולה.
        
        :return: מחרוזת המציינת את הפעולה הבאה (למשל: "start", "stats", "settings", "exit").
        """
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(settings.FPS) / 1000.0

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.next_action = "exit"
                    self.running = False

            # עדכון מצב הכפתורים
            for btn in self.buttons:
                btn.update(events)

            # ציור
            self.screen.fill((30, 30, 30))  # רקע אפור כהה
            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()

        # מחזיר את הפעולה שהמשתמש בחר
        return self.next_action
