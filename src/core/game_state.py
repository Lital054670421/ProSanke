"""
game_state.py

This module manages the game states (running, paused, game_over) and implements an Observer mechanism
to notify subscribed modules when the game state changes.
"""

import enum
from abc import ABC, abstractmethod
from typing import List

# --------------------------------------------------------------------
# Enum for game states
# --------------------------------------------------------------------
class GameState(enum.Enum):
    """
    מייצג את מצבי המשחק השונים.
    """
    RUNNING = "running"      # מצב משחק פעיל
    PAUSED = "paused"        # מצב השהייה
    GAME_OVER = "game_over"  # מצב סיום משחק

# --------------------------------------------------------------------
# Observer interface for game state changes
# --------------------------------------------------------------------
class GameStateObserver(ABC):
    """
    ממשק למנויים שמעוניינים לקבל התראה על שינוי במצב המשחק.
    """

    @abstractmethod
    def on_game_state_change(self, new_state: GameState) -> None:
        """
        מתודה שמופעלת כאשר מצב המשחק משתנה.
        :param new_state: המצב החדש של המשחק.
        """
        pass

# --------------------------------------------------------------------
# GameStateManager: Manages the current game state and notifies observers
# --------------------------------------------------------------------
class GameStateManager:
    """
    מנהל את המצב הנוכחי של המשחק ומודיע לכל המנויים (observers) על כל שינוי במצב.
    """

    def __init__(self, initial_state: GameState = GameState.RUNNING):
        """
        מאתחל את מנהל מצב המשחק עם מצב התחלתי.
        :param initial_state: המצב ההתחלתי של המשחק (ברירת מחדל: RUNNING).
        """
        self._current_state: GameState = initial_state
        self._observers: List[GameStateObserver] = []  # רשימת המנויים

    def subscribe(self, observer: GameStateObserver) -> None:
        """
        מוסיף מנוי (observer) לרשימה לקבלת עדכונים על שינוי במצב.
        :param observer: מופע של GameStateObserver.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: GameStateObserver) -> None:
        """
        מסיר מנוי מהרשימה.
        :param observer: מופע של GameStateObserver שיש להסיר.
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def set_state(self, new_state: GameState) -> None:
        """
        משנה את מצב המשחק הנוכחי ומודיע לכל המנויים.
        :param new_state: המצב החדש שאליו יש לעבור.
        """
        if new_state != self._current_state:
            self._current_state = new_state
            self._notify_observers()

    def get_state(self) -> GameState:
        """
        מחזיר את מצב המשחק הנוכחי.
        :return: מצב המשחק הנוכחי.
        """
        return self._current_state

    def _notify_observers(self) -> None:
        """
        מעדכן את כל המנויים במצב החדש.
        """
        for observer in self._observers:
            observer.on_game_state_change(self._current_state)

