import csv
import os

class ScoreManager:
    def __init__(self):
        self.filename = os.path.join(os.path.dirname(__file__), "scores.csv")
        self.difficulty_multipliers = {
            1: 1,  # Facile
            2: 2,  # Normal
            3: 3,  # Difficile
            4: 4   # Expert
        }
        self._create_file_not_exists()

    def _create_file_not_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Nom", "Points"])

    def save_score(self, player_name, difficulty, moves):
        """Enregistre uniquement le nom et le score total"""
        score = self.calculate_score(difficulty, moves)
        
        # Lecture des scores existants
        scores = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        scores[row[0]] = int(row[1])

        # Mise à jour du score
        if player_name in scores:
            scores[player_name] += score
        else:
            scores[player_name] = score

        # Réécriture du fichier
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nom", "Points"])
            writer.writerows(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    def calculate_score(self, difficulty, moves):
        """Calcule le score avec le multiplicateur de difficulté"""
        multiplier = self.difficulty_multipliers.get(difficulty, 1)
        return max(multiplier * (100 - moves), 0)

    def get_scores(self):
        """Retourne la liste des scores (nom, points) triée par score décroissant"""
        scores = []
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        scores.append((row[0], int(row[1])))
        except FileNotFoundError:
            pass
        return scores
