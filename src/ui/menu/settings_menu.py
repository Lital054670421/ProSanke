"""
settings_menu.py

ממשק הגדרות המאפשר למשתמש להתאים את אפשרויות המשחק:
- הפעלה/כיבוי מוזיקת רקע
- בחירת רמת קושי (Easy, Medium, Hard)
- בחירת ערכת נושא (Default, Modern)

הממשק טוען את ההגדרות דרך config_parser ומאחסן שינויים בקובץ קונפיגורציה.
הקוד נכתב בצורה מודולרית ומובנה, כך שיהיה קל להרחבה ותחזוקה.
"""

import sys
import pygame
import config.config_parser as config_parser
import config.settings as settings

# ודא שהמשתנה CONFIG_FILE_PATH מוגדר, אם לא – הגדר ערך ברירת מחדל
try:
    CONFIG_FILE_PATH = settings.CONFIG_FILE_PATH
except AttributeError:
    CONFIG_FILE_PATH = "config/config.json"


class Button:
    """
    כפתור כללי לשימוש בממשק ההגדרות.
    
    מאפיינים:
      - text: הטקסט שמוצג על הכפתור.
      - rect: האזור (מיקום ומידות) של הכפתור.
      - font: הפונט להצגת הטקסט.
      - on_click: פונקציה שתופעל בלחיצה על הכפתור.
      - text_color, bg_color, hover_color: צבעי טקסט, רקע ומצב ריחוף.
    """
    def __init__(self, text: str, rect: pygame.Rect, font: pygame.font.Font,
                 on_click: callable, text_color=(255, 255, 255),
                 bg_color=(0, 0, 0), hover_color=(50, 50, 50)):
        self.text = text
        self.rect = rect
        self.font = font
        self.on_click = on_click
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את הכפתור על משטח התצוגה.
        במצב ריחוף (hover) משתמש בצבע hover, אחרת בצבע הרקע.
        """
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, events: list) -> None:
        """
        בודק עדכון עבור מצב ריחוף ולחיצות עכבר.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.on_click()


class SettingsMenu:
    """
    מחלקת SettingsMenu מציגה תפריט הגדרות שמאפשר:
      - הפעלה/כיבוי מוזיקת רקע.
      - בחירת רמת קושי.
      - בחירת ערכת נושא.
    
    ההגדרות נטענות ונשמרות דרך config_parser, כך ששינויים יישמרו באופן קבוע.
    """
    def __init__(self, screen: pygame.Surface, config_file: str = CONFIG_FILE_PATH) -> None:
        self.screen = screen
        self.config_file = config_file

        # טוען את הקונפיגורציה מהקובץ החיצוני
        try:
            self.config = config_parser.load_config(self.config_file)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

        # מוודא שהמפתחות הדרושים קיימים – אם לא, משתמש בערכי ברירת המחדל מה-settings
        self.config.setdefault("BACKGROUND_MUSIC", getattr(settings, "BACKGROUND_MUSIC", True))
        self.config.setdefault("DIFFICULTY", getattr(settings, "DIFFICULTY", "easy"))
        self.config.setdefault("THEME", getattr(settings, "THEME", "default"))

        # אתחול הפונט והכפתורים
        self.font = pygame.font.Font(settings.SNAKE_FONT_PATH, 32)
        self.buttons = []
        self.running = True
        self.create_buttons()

    def create_buttons(self) -> None:
        """
        יוצר את כל הכפתורים בתפריט:
          - כפתור להפעלת/כיבוי מוזיקת רקע.
          - כפתורי בחירת רמת קושי.
          - כפתורי בחירת ערכת נושא.
          - כפתור Save & Return.
        """
        screen_width, screen_height = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        center_x = screen_width // 2

        start_y = 150
        btn_width = 300
        btn_height = 50
        gap = 80

        # כפתור הפעלת/כיבוי מוזיקת רקע
        def toggle_music():
            self.config["BACKGROUND_MUSIC"] = not self.config["BACKGROUND_MUSIC"]
            # עדכון הטקסט על הכפתור בהתאם למצב החדש
            bg_music_button.text = f"Background Music: {'On' if self.config['BACKGROUND_MUSIC'] else 'Off'}"

        bg_music_button = Button(
            text=f"Background Music: {'On' if self.config['BACKGROUND_MUSIC'] else 'Off'}",
            rect=pygame.Rect(center_x - btn_width // 2, start_y, btn_width, btn_height),
            font=self.font,
            on_click=toggle_music,
            bg_color=(0, 100, 100),
            hover_color=(0, 150, 150)
        )
        self.buttons.append(bg_music_button)

        # כפתורי בחירת רמת קושי
        difficulty_options = ["easy", "medium", "hard"]
        diff_btn_width = 100
        diff_gap = 20
        diff_start_x = center_x - (len(difficulty_options) * diff_btn_width + (len(difficulty_options) - 1) * diff_gap) // 2

        for i, level in enumerate(difficulty_options):
            def make_diff_click(lvl):
                def set_difficulty():
                    self.config["DIFFICULTY"] = lvl
                    # עדכון צבעי הכפתורים לפי הבחירה הנוכחית
                    for btn in self.buttons:
                        if hasattr(btn, 'difficulty_option'):
                            btn.bg_color = (100, 0, 100) if btn.difficulty_option == self.config["DIFFICULTY"] else (50, 0, 50)
                return set_difficulty

            diff_button = Button(
                text=level.capitalize(),
                rect=pygame.Rect(diff_start_x + i * (diff_btn_width + diff_gap), start_y + gap, diff_btn_width, btn_height),
                font=self.font,
                on_click=make_diff_click(level),
                bg_color=(100, 0, 100) if self.config["DIFFICULTY"] == level else (50, 0, 50),
                hover_color=(150, 0, 150)
            )
            diff_button.difficulty_option = level  # תכונה מותאמת אישית לזיהוי
            self.buttons.append(diff_button)

        # כפתורי בחירת ערכת נושא
        theme_options = ["default", "modern"]
        theme_btn_width = 150
        theme_gap = 20
        theme_start_x = center_x - (len(theme_options) * theme_btn_width + (len(theme_options) - 1) * theme_gap) // 2

        for i, theme_option in enumerate(theme_options):
            def make_theme_click(th):
                def set_theme():
                    self.config["THEME"] = th
                    for btn in self.buttons:
                        if hasattr(btn, 'theme_option'):
                            btn.bg_color = (0, 100, 0) if btn.theme_option == self.config["THEME"] else (0, 50, 0)
                return set_theme

            theme_button = Button(
                text=theme_option.capitalize(),
                rect=pygame.Rect(theme_start_x + i * (theme_btn_width + theme_gap), start_y + 2 * gap, theme_btn_width, btn_height),
                font=self.font,
                on_click=make_theme_click(theme_option),
                bg_color=(0, 100, 0) if self.config["THEME"] == theme_option else (0, 50, 0),
                hover_color=(0, 150, 0)
            )
            theme_button.theme_option = theme_option
            self.buttons.append(theme_button)

        # כפתור Save & Return
        def save_and_return():
            try:
                config_parser.save_config(self.config, self.config_file)
                print("Configuration saved successfully.")
            except Exception as e:
                print(f"Error saving config: {e}")
            self.running = False

        save_button = Button(
            text="Save & Return",
            rect=pygame.Rect(center_x - btn_width // 2, start_y + 3 * gap, btn_width, btn_height),
            font=self.font,
            on_click=save_and_return,
            bg_color=(100, 100, 0),
            hover_color=(150, 150, 0)
        )
        self.buttons.append(save_button)

    def run(self) -> None:
        """
        מפעיל את לולאת תפריט ההגדרות עד שהמשתמש מסיים (בלחיצה על Save & Return).
        """
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(settings.FPS) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # עדכון כל הכפתורים
            for btn in self.buttons:
                btn.update(events)

            # ציור המסך
            self.screen.fill((20, 20, 20))
            title_surf = self.font.render("Settings", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 80))
            self.screen.blit(title_surf, title_rect)

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()
        return
