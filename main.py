from game_engine import GameState
from display_game import SokobanGUI
from database import ScoreDatabase

if __name__ == "__main__":
    game_state = GameState("levels/level1.txt")
    gui = SokobanGUI(game_state)
    gui.run()
