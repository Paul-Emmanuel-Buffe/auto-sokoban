class Grid:
    def __init__(self, matrix):
        self.matrix = matrix
        self.player_pos = self.find_player()

    def find_player(self):
        # Cherche la position du joueur dans la grille
        pass

    def move_player(self, direction):
        # Déplace le joueur dans la direction spécifiée
        pass

    def is_victory(self):
        # Vérifie si toutes les caisses sont sur les cibles
        pass

    def reset(self):
        # Réinitialise la grille
        pass

    def undo_last_move(self):
        # Annule le dernier déplacement
        pass


class GameState:
    def __init__(self, level_path):
        self.grid = self.load_level(level_path)
        self.move_history = []

    def load_level(self, path):
        # Charge la matrice du niveau depuis un fichier
        pass

    def move(self, direction):
        # Applique le mouvement si possible
        pass

    def undo(self):
        # Annule le dernier coup
        pass

    def reset(self):
        # Réinitialise la partie
        pass

    def get_grid(self):
        return self.grid
