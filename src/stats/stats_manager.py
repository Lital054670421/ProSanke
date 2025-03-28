"""
stats_manager.py

This module provides the StatsManager class for managing game statistics and achievements.
It loads and saves statistics data (score, total games, total play time, achievements, and scoreboard)
from/to a JSON file in the user data directory, using the 'platformdirs' library.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional
from platformdirs import user_data_dir

# Define application constants for user data directory
APP_NAME = "SnakeGame"
APP_AUTHOR = "MyCompany"

class StatsManager:
    _instance = None  # Singleton instance

    def __new__(cls, username: str = "Player", achievement_callback: Optional[callable] = None) -> "StatsManager":
        if cls._instance is None:
            cls._instance = super(StatsManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, username: str = "Player", achievement_callback: Optional[callable] = None) -> None:
        # Only initialize once
        if hasattr(self, "initialized") and self.initialized:
            return

        self.username = username

        # Determine the user data directory using platformdirs
        data_dir = user_data_dir(appname=APP_NAME, appauthor=APP_AUTHOR, roaming=True)
        os.makedirs(data_dir, exist_ok=True)

        # Create a unique stats file per user (spaces replaced with underscores)
        safe_name = self.username.replace(" ", "_")
        self.stats_file = os.path.join(data_dir, f"stats_{safe_name}.json")
        print(f"[StatsManager] Using stats file: {self.stats_file}")

        # Initial statistics data
        self.data: Dict[str, Any] = {
            "highest_score": 0,
            "total_games": 0,
            "total_time": 0.0,
            "scoreboard": [],   # List of dicts: [{"player_name": str, "score": int}, ...]
            "achievements": []  # List of achievement strings
        }
        self.achievement_callback = achievement_callback
        self.load_stats()
        self.initialized = True

    def load_stats(self) -> None:
        """
        Loads statistics data from the JSON file. If it doesn't exist, creates one with default values.
        """
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                print(f"[StatsManager] Loaded stats: {self.data}")
            except Exception as e:
                print(f"[StatsManager] Error loading stats from file: {e}")
        else:
            print("[StatsManager] Stats file not found, creating new one.")
            self.save_stats()

    def save_stats(self) -> None:
        """
        Saves the current statistics data to the JSON file.
        """
        try:
            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            print(f"[StatsManager] Stats saved successfully to {self.stats_file}")
        except Exception as e:
            print(f"[StatsManager] Error saving stats to file: {e}")

    def update_game_result(self, score: int, play_time: float, player_name: str = "Player") -> None:
        """
        Updates the statistics after a game finishes.
        
        :param score: The score achieved in the game.
        :param play_time: The duration of the game in seconds.
        :param player_name: The name of the player.
        """
        self.data["total_games"] += 1
        self.data["total_time"] += play_time

        if score > self.data["highest_score"]:
            self.data["highest_score"] = score

        # Update scoreboard: limit to top 10 entries
        self.data["scoreboard"].append({"player_name": player_name, "score": score})
        self.data["scoreboard"].sort(key=lambda x: x["score"], reverse=True)
        self.data["scoreboard"] = self.data["scoreboard"][:10]

        # Evaluate and update achievements based on game results
        self.check_achievements(score, play_time)

        # Save updated statistics
        self.save_stats()

    def check_achievements(self, score: int, play_time: float) -> None:
        """
        Checks and updates achievements based on current game results.
        Unlocks new achievements if criteria are met.

        This version adds more achievements for score milestones (50,200,500).
        You can also add more time-based or total-games-based criteria below.
        """
        new_achievements = []

        # --- Score-based achievements ---
        if score >= 50 and "Score 50+" not in self.data["achievements"]:
            new_achievements.append("Score 50+")
        if score >= 200 and "Score 200+" not in self.data["achievements"]:
            new_achievements.append("Score 200+")
        if score >= 500 and "Score 500+" not in self.data["achievements"]:
            new_achievements.append("Score 500+")

        # --- Time-based achievements ---
        if play_time >= 300 and "5 Minutes Survival" not in self.data["achievements"]:
            new_achievements.append("5 Minutes Survival")

        # --- Number of total games played (already present) ---
        if self.data["total_games"] >= 10 and "Veteran Player" not in self.data["achievements"]:
            new_achievements.append("Veteran Player")

        # Add them if new, print message, call callback
        for achievement in new_achievements:
            self.data["achievements"].append(achievement)
            print(f"[StatsManager] Achievement unlocked: {achievement}")
            if self.achievement_callback:
                self.achievement_callback(achievement)

    def get_highest_score(self) -> int:
        return self.data.get("highest_score", 0)

    def get_total_games(self) -> int:
        return self.data.get("total_games", 0)

    def get_total_time_played(self) -> float:
        return self.data.get("total_time", 0.0)

    def get_achievements(self) -> List[str]:
        return self.data.get("achievements", [])

    def get_scoreboard(self) -> List[dict]:
        return self.data.get("scoreboard", [])


# For testing purposes:
if __name__ == "__main__":
    def achievement_notification(achievement: str) -> None:
        print(f"[Notification] New Achievement Unlocked: {achievement}")

    manager = StatsManager(username="Player", achievement_callback=achievement_notification)
    manager.update_game_result(score=600, play_time=180, player_name="Player")
    manager.update_game_result(score=400, play_time=350, player_name="Player")
    
    print("Highest Score:", manager.get_highest_score())
    print("Total Games:", manager.get_total_games())
    print("Total Time Played:", manager.get_total_time_played())
    print("Achievements:", manager.get_achievements())
    print("Scoreboard:", manager.get_scoreboard())
