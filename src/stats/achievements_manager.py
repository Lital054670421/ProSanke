"""
achievements_manager.py

This module provides the AchievementsManager class which tracks and evaluates achievements
based on user performance in the Snake game.

In this extended version, we focus on achievements triggered by total score or
apples eaten. Each time we call `evaluate`, we pass the updated game stats,
and any newly unlocked achievements are returned for further handling.
"""

from typing import List, Dict, Any


class AchievementsManager:
    def __init__(self) -> None:
        """
        Initializes the AchievementsManager with an empty set of achievements.
        """
        # Maintain achievements in a set for quick lookup
        self.unlocked: set[str] = set()

    def evaluate(self, game_stats: Dict[str, Any]) -> List[str]:
        """
        Evaluates the current game statistics and updates unlocked achievements.

        :param game_stats: Dictionary containing cumulative game statistics, e.g.,
            {
                "score": int,         # total cumulative score
                "apples_eaten": int,  # total apples eaten
                "play_time": float,   # total time played (seconds)
                ...
            }
        :return: List of achievements that are newly unlocked during this evaluation.
        """
        new_achievements: List[str] = []

        # Extract relevant stats
        score = game_stats.get("score", 0)
        apples = game_stats.get("apples_eaten", 0)
        play_time = game_stats.get("play_time", 0.0)

        # Example achievements by total score
        if score >= 50 and "Score 50+" not in self.unlocked:
            new_achievements.append("Score 50+")
        if score >= 200 and "Score 200+" not in self.unlocked:
            new_achievements.append("Score 200+")
        if score >= 500 and "Score 500+" not in self.unlocked:
            new_achievements.append("Score 500+")

        # Example achievements by apples eaten
        if apples >= 1 and "First Apple" not in self.unlocked:
            new_achievements.append("First Apple")
        if apples >= 10 and "Rookie Eater" not in self.unlocked:
            new_achievements.append("Rookie Eater")
        if apples >= 50 and "Pro Eater" not in self.unlocked:
            new_achievements.append("Pro Eater")

        # Example achievements by total play time
        if play_time >= 300 and "Marathon Survivor" not in self.unlocked:
            new_achievements.append("Marathon Survivor")

        # Mark all newly unlocked
        for achv in new_achievements:
            self.unlocked.add(achv)

        return new_achievements

    def get_unlocked(self) -> List[str]:
        """
        Returns a list of all unlocked achievements.
        """
        return list(self.unlocked)
