import sqlite3

class ScoreDatabase:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        # Crée la table des scores si elle n'existe pas
        pass

    def save_score(self, username, moves, time):
        # Insère un score dans la base
        pass

    def get_leaderboard(self):
        # Récupère les meilleurs scores
        pass
