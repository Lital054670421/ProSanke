"""
settings_menu.py

ממשק הגדרות המאפשר למשתמש להתאים את אפשרויות המשחק:
- הפעלה/כיבוי מוזיקת רקע.
- שליטה בעוצמת הקול של המוזיקה באמצעות סליידר.
- בחירת רמת קושי (Easy, Medium, Hard).
- בחירת ערכת נושא (Default, Modern).

הממשק טוען את ההגדרות דרך config_parser ומאחסן שינויים בקובץ הקונפיגורציה.
"""

import sys
import pygame
import config.config_parser as config_parser
import config.settings as settings

try:
    CONFIG_FILE_PATH = settings.CONFIG_FILE_PATH
except AttributeError:
    CONFIG_FILE_PATH = "config/config.json"

# Import SoundManager
from src.audio.sound_manager import SoundManager

class Button:
    """
    כפתור כללי לשימוש בממשק ההגדרות.
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
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, events: list) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.on_click()

class Slider:
    """
    סליידר לשליטה בעוצמת המוזיקה.

    מציג מסלול (track) עם ידית (handle) שניתן לגרור. הערך מחושב כיחס בין
    המיקום של הידית לאורך המסלול. הערך יהיה בין min_val ל-max_val.
    """
    def __init__(self, x: int, y: int, width: int, height: int,
                 min_val: float = 0.0, max_val: float = 1.0, initial_val: float = 0.6,
                 track_color: tuple = (200, 200, 200), handle_color: tuple = (255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height  # גובה המסלול
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.track_color = track_color
        self.handle_color = handle_color

        self.handle_radius = max(10, height // 2 + 4)
        self.dragging = False

    def _handle_rect(self) -> pygame.Rect:
        """
        מחזיר pygame.Rect שמייצג את אזור הידית, לצורך בדיקת לחיצה.
        """
        handle_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        handle_y = self.y + self.height // 2
        return pygame.Rect(handle_x - self.handle_radius,
                           handle_y - self.handle_radius,
                           self.handle_radius * 2,
                           self.handle_radius * 2)

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        מעבד אירועי עכבר כדי לבדוק לחיצה וגרירה של הידית.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self._handle_rect().collidepoint(mx, my):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def update(self) -> None:
        """
        אם הידית נגררת, מחשב את הערך בהתאם למיקום העכבר.
        """
        if self.dragging:
            mx, _ = pygame.mouse.get_pos()
            relative_x = mx - self.x
            if relative_x < 0:
                relative_x = 0
            elif relative_x > self.width:
                relative_x = self.width
            ratio = relative_x / self.width
            self.value = self.min_val + (self.max_val - self.min_val) * ratio

    def draw(self, surface: pygame.Surface) -> None:
        """
        מצייר את המסלול והידית של הסליידר.
        """
        track_rect = pygame.Rect(self.x, self.y + self.height // 2 - 2, self.width, 4)
        pygame.draw.rect(surface, self.track_color, track_rect)
        handle_x = self.x + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        handle_y = self.y + self.height // 2
        pygame.draw.circle(surface, self.handle_color, (handle_x, handle_y), self.handle_radius)
        # לא מציגים את הערך, כפי שהתבקש

class SettingsMenu:
    """
    מחלקת SettingsMenu מציגה תפריט הגדרות שמאפשר:
      - הפעלה/כיבוי מוזיקת רקע.
      - שליטה בעוצמת הקול באמצעות סליידר.
      - בחירת רמת קושי.
      - בחירת ערכת נושא.
      
    ההגדרות נטענות ונשמרות דרך config_parser.
    """
    def __init__(self, screen: pygame.Surface, config_file: str = CONFIG_FILE_PATH) -> None:
        self.screen = screen
        self.config_file = config_file

        try:
            self.config = config_parser.load_config(self.config_file)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

        self.config.setdefault("BACKGROUND_MUSIC", getattr(settings, "BACKGROUND_MUSIC", True))
        self.config.setdefault("MUSIC_VOLUME", getattr(settings, "MUSIC_VOLUME", 0.6))
        self.config.setdefault("DIFFICULTY", getattr(settings, "DIFFICULTY", "easy"))
        self.config.setdefault("THEME", getattr(settings, "THEME", "default"))

        self.font = pygame.font.Font(settings.SNAKE_FONT_PATH, 32)
        self.buttons = []
        self.running = True

        self.sound_manager = SoundManager()
        self.sound_manager.set_volume(self.config["MUSIC_VOLUME"])

        slider_x = (settings.SCREEN_WIDTH - 300) // 2
        slider_y = 150 + 80  # מתחת לכפתור המוזיקה
        self.volume_slider = Slider(slider_x, slider_y, 300, 20, initial_val=self.config["MUSIC_VOLUME"])

        self.create_buttons()

    def create_buttons(self) -> None:
        screen_width, screen_height = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        center_x = screen_width // 2
        start_y = 150
        btn_width = 300
        btn_height = 50
        gap = 80

        def toggle_music():
            self.config["BACKGROUND_MUSIC"] = not self.config["BACKGROUND_MUSIC"]
            bg_music_button.text = f"Background Music: {'On' if self.config['BACKGROUND_MUSIC'] else 'Off'}"
            if self.config["BACKGROUND_MUSIC"]:
                self.sound_manager.play_music()
            else:
                self.sound_manager.stop_music()

        bg_music_button = Button(
            text=f"Background Music: {'On' if self.config['BACKGROUND_MUSIC'] else 'Off'}",
            rect=pygame.Rect(center_x - btn_width // 2, start_y, btn_width, btn_height),
            font=self.font,
            on_click=toggle_music,
            bg_color=(0, 100, 100),
            hover_color=(0, 150, 150)
        )
        self.buttons.append(bg_music_button)

        difficulty_options = ["easy", "medium", "hard"]
        diff_btn_width = 100
        diff_gap = 20
        diff_start_x = center_x - (len(difficulty_options) * diff_btn_width + (len(difficulty_options) - 1) * diff_gap) // 2

        for i, level in enumerate(difficulty_options):
            def make_diff_click(lvl):
                def set_difficulty():
                    self.config["DIFFICULTY"] = lvl
                    for btn in self.buttons:
                        if hasattr(btn, 'difficulty_option'):
                            btn.bg_color = (100, 0, 100) if btn.difficulty_option == self.config["DIFFICULTY"] else (50, 0, 50)
                return set_difficulty

            diff_button = Button(
                text=level.capitalize(),
                rect=pygame.Rect(diff_start_x + i * (diff_btn_width + diff_gap), start_y + 2 * gap, diff_btn_width, btn_height),
                font=self.font,
                on_click=make_diff_click(level),
                bg_color=(100, 0, 100) if self.config["DIFFICULTY"] == level else (50, 0, 50),
                hover_color=(150, 0, 150)
            )
            diff_button.difficulty_option = level
            self.buttons.append(diff_button)

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
                rect=pygame.Rect(theme_start_x + i * (theme_btn_width + theme_gap), start_y + 3 * gap, theme_btn_width, btn_height),
                font=self.font,
                on_click=make_theme_click(theme_option),
                bg_color=(0, 100, 0) if self.config["THEME"] == theme_option else (0, 50, 0),
                hover_color=(0, 150, 0)
            )
            theme_button.theme_option = theme_option
            self.buttons.append(theme_button)

        def save_and_return():
            self.config["MUSIC_VOLUME"] = self.volume_slider.value
            self.sound_manager.set_volume(self.volume_slider.value)
            try:
                config_parser.save_config(self.config, self.config_file)
                print("Configuration saved successfully.")
            except Exception as e:
                print(f"Error saving config: {e}")
            self.running = False

        save_button = Button(
            text="Save & Return",
            rect=pygame.Rect(center_x - btn_width // 2, start_y + 4 * gap, btn_width, btn_height),
            font=self.font,
            on_click=save_and_return,
            bg_color=(100, 100, 0),
            hover_color=(150, 150, 0)
        )
        self.buttons.append(save_button)

    def run(self) -> None:
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(settings.FPS) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # מעבירים את אותם אירועים לסליידר ולכפתורים
            for event in events:
                self.volume_slider.handle_event(event)
            self.volume_slider.update()

            for btn in self.buttons:
                btn.update(events)

            # עדכון מידי של עוצמת הקול
            self.sound_manager.set_volume(self.volume_slider.value)

            self.screen.fill((20, 20, 20))
            title_surf = self.font.render("Settings", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(settings.SCREEN_WIDTH // 2, 80))
            self.screen.blit(title_surf, title_rect)

            for btn in self.buttons:
                btn.draw(self.screen)

            self.volume_slider.draw(self.screen)
                
            pygame.display.flip()
