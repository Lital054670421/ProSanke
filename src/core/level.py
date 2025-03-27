"""
level.py

This module manages the game difficulty levels using the Strategy design pattern.
It defines an abstract base class (DifficultyStrategy) for difficulty strategies,
concrete implementations for different difficulty levels (Easy, Medium, Hard),
and a LevelManager that dynamically adjusts the game parameters based on the current score.
"""

from abc import ABC, abstractmethod

# --------------------------------------------------------------------
# Abstract Base Class for Difficulty Strategies
# --------------------------------------------------------------------
class DifficultyStrategy(ABC):
    """
    ממשק בסיסי (Abstract Base Class) עבור אסטרטגיות קושי.
    מגדיר את המתודות שעל כל אסטרטגיה לממש על מנת לקבוע פרמטרים כגון מהירות הנחש ותדירות הופעת המכשולים.
    """
    
    @abstractmethod
    def get_snake_speed(self) -> int:
        """
        מחזיר את מהירות הנחש עבור רמת הקושי הנוכחית.
        :return: מהירות הנחש (בפיקסלים לעדכון, לדוגמה).
        """
        pass

    @abstractmethod
    def get_obstacle_frequency(self) -> float:
        """
        מחזיר את תדירות הופעת המכשולים עבור רמת הקושי הנוכחית.
        :return: תדירות המכשולים (לדוגמה, מספר מכשולים לשנייה או ערך יחסי אחר).
        """
        pass

# --------------------------------------------------------------------
# Concrete Difficulty Strategies
# --------------------------------------------------------------------
class EasyStrategy(DifficultyStrategy):
    """
    אסטרטגיית קושי קלה – מהירות נמוכה ותדירות מופחתת של מכשולים.
    """
    def get_snake_speed(self) -> int:
        return 10  # מהירות נמוכה, לדוגמה 10 פיקסלים לעדכון

    def get_obstacle_frequency(self) -> float:
        return 0.1  # תדירות נמוכה של מכשולים (לדוגמה, 0.1 יחידות)

class MediumStrategy(DifficultyStrategy):
    """
    אסטרטגיית קושי בינונית – מהירות מתונה ותדירות מכשולים בינונית.
    """
    def get_snake_speed(self) -> int:
        return 15  # מהירות בינונית

    def get_obstacle_frequency(self) -> float:
        return 0.3  # תדירות מכשולים בינונית

class HardStrategy(DifficultyStrategy):
    """
    אסטרטגיית קושי קשה – מהירות גבוהה ותדירות מכשולים מוגברת.
    """
    def get_snake_speed(self) -> int:
        return 20  # מהירות גבוהה

    def get_obstacle_frequency(self) -> float:
        return 0.5  # תדירות גבוהה של מכשולים

# --------------------------------------------------------------------
# LevelManager: Manages current difficulty level and strategy switching
# --------------------------------------------------------------------
class LevelManager:
    """
    מנהל רמות הקושי של המשחק. 
    מתעדכן על פי התקדמות המשחק (למשל, הציון של השחקן) ומשנה את אסטרטגיית הקושי בהתאם.
    
    בדוגמה זו, נשתמש בערכי סף (thresholds) לציון כדי להחליף בין אסטרטגיות:
      - ציון נמוך: EasyStrategy
      - ציון בינוני: MediumStrategy
      - ציון גבוה: HardStrategy
    """
    
    def __init__(self, initial_score: int = 0) -> None:
        """
        אתחול מנהל הרמות עם ציון התחלתי ואסטרטגיית קושי ראשונית.
        
        :param initial_score: הציון ההתחלתי של השחקן (ברירת מחדל 0).
        """
        self.score: int = initial_score
        self.strategy: DifficultyStrategy = EasyStrategy()  # ברירת מחדל: קושי קל

    def update_score(self, new_score: int) -> None:
        """
        מעדכן את הציון הנוכחי ומחליף את אסטרטגיית הקושי בהתאם לסף הציון.
        
        :param new_score: הציון החדש של השחקן.
        """
        self.score = new_score
        if self.score < 50:
            self.strategy = EasyStrategy()
        elif self.score < 100:
            self.strategy = MediumStrategy()
        else:
            self.strategy = HardStrategy()

    def get_parameters(self) -> dict:
        """
        מחזיר מילון המכיל את הפרמטרים הנוכחיים של רמת הקושי,
        כגון מהירות הנחש ותדירות הופעת המכשולים.
        
        :return: מילון עם המפתחות "snake_speed" ו-"obstacle_frequency".
        """
        return {
            "snake_speed": self.strategy.get_snake_speed(),
            "obstacle_frequency": self.strategy.get_obstacle_frequency()
        }
