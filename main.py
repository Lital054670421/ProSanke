import pygame
from src.core.game_logic import GameLogic

def main():
    # אתחול pygame
    pygame.init()
    
    # יצירת מופע של GameLogic והפעלת המשחק
    game = GameLogic()
    game.run()

if __name__ == "__main__":
    main()
