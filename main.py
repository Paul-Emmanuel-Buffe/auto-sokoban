import pygame
import sys
from display_game import SokobanDisplay


def main():
    """Fonction principale simplifiée"""
    game = SokobanDisplay()
    game.start_game()
    

if __name__ == "__main__":
    main()