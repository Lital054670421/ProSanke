"""
statistics_menu.py

This module provides a StatisticsMenu class that displays game statistics,
a scoreboard, and achievements in a visually clear manner.
It integrates with StatsManager to fetch data in real-time.
"""

import pygame
from typing import List, Tuple, Callable, Optional
import config.settings as settings

# Import unified UI components
from src.ui.ui_components import Button

# נניח שיש לך מחלקה stats_manager.py שאוספת נתונים מהמשחק
from src.stats.stats_manager import StatsManager

class StatisticsMenu:
    """
    תפריט סטטיסטיקות שמציג:
     - ניקוד גבוה
     - מספר משחקים
     - זמן משחק מצטבר
     - רשימת הישגים (Achievements)
     - לוח תוצאות (Scoreboard)
    מקבל StatsManager לצורך שליפת המידע בזמן אמת.
    """
    def __init__(self, screen: pygame.Surface, stats_manager: StatsManager):
        """
        אתחל את תפריט הסטטיסטיקות.
        
        :param screen: משטח התצוגה (pygame.Surface).
        :param stats_manager: מופע StatsManager שמספק את נתוני הסטטיסטיקות.
        """
        self.screen = screen
        self.stats_manager = stats_manager
        self.font = pygame.font.Font(settings.SNAKE_FONT_PATH, 32)

        # כפתור חזרה
        btn_width, btn_height = 200, 60
        self.back_button = Button(
            text="Back",
            rect=pygame.Rect((settings.SCREEN_WIDTH - btn_width) // 2,
                             settings.SCREEN_HEIGHT - btn_height - 50,
                             btn_width, btn_height),
            font=self.font,
            on_click=self.on_back_clicked,
            text_color=(255, 255, 255),
            bg_color=(100, 0, 0),
            hover_color=(150, 0, 0)
        )

        self.running = True
        self.next_action: Optional[str] = None  # מה נעשה אחרי הסטטיסטיקות, למשל לחזור לתפריט

    def on_back_clicked(self):
        """
        פונקציה שמופעלת כשלוחצים על כפתור Back (חזרה).
        """
        self.next_action = "back"
        self.running = False

    def run(self) -> str:
        """
        מציג את תפריט הסטטיסטיקות עד שהמשתמש בוחר לחזור.
        
        :return: "back" אם המשתמש בחר לחזור לתפריט הראשי או פעולה אחרת בעתיד.
        """
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(settings.FPS) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.next_action = "exit"
                    self.running = False

            # עדכון כפתור החזרה
            self.back_button.update(events)

            # ציור
            self.screen.fill((30, 30, 30))  # רקע אפור

            self.draw_statistics()

            # ציור הכפתור
            self.back_button.draw(self.screen)

            pygame.display.flip()

        return self.next_action if self.next_action else "back"

    def draw_statistics(self) -> None:
        """
        מצייר את טקסט הסטטיסטיקות, לוח תוצאות והישגים על המסך.
        """
        # שליפת נתונים לדוגמה:
        highest_score = self.stats_manager.get_highest_score()
        total_games = self.stats_manager.get_total_games()
        total_time = self.stats_manager.get_total_time_played()
        achievements_list = self.stats_manager.get_achievements()
        scoreboard = self.stats_manager.get_scoreboard()

        # ציור כותרת
        title_surf = self.font.render("Statistics", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_surf, title_rect)

        # ניקוד גבוה
        high_score_txt = f"Highest Score: {highest_score}"
        high_score_surf = self.font.render(high_score_txt, True, (255, 255, 255))
        self.screen.blit(high_score_surf, (50, 120))

        # מספר משחקים
        total_games_txt = f"Total Games: {total_games}"
        total_games_surf = self.font.render(total_games_txt, True, (255, 255, 255))
        self.screen.blit(total_games_surf, (50, 170))

        # זמן משחק מצטבר
        total_time_txt = f"Total Time Played: {round(total_time, 2)} seconds"
        total_time_surf = self.font.render(total_time_txt, True, (255, 255, 255))
        self.screen.blit(total_time_surf, (50, 220))

        # הישגים (Achievements)
        achievements_y = 270
        achievements_title = self.font.render("Achievements:", True, (255, 255, 255))
        self.screen.blit(achievements_title, (50, achievements_y))
        achievements_y += 40
        for ach in achievements_list:
            line_surf = self.font.render(f"- {ach}", True, (200, 200, 200))
            self.screen.blit(line_surf, (70, achievements_y))
            achievements_y += 40

        # לוח תוצאות (scoreboard)
        scoreboard_y = achievements_y + 40
        scoreboard_title = self.font.render("Scoreboard:", True, (255, 255, 255))
        self.screen.blit(scoreboard_title, (50, scoreboard_y))
        scoreboard_y += 40

        for idx, score_entry in enumerate(scoreboard, start=1):
            # נניח ש-score_entry זה tuple (player_name, score)
            player_name, score = score_entry
            line_surf = self.font.render(f"{idx}. {player_name}: {score}", True, (200, 200, 200))
            self.screen.blit(line_surf, (70, scoreboard_y))
            scoreboard_y += 40
