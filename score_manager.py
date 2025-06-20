
# Classe de gestion du scoreboard

class ScoreManager:
    def __init__(self):
        
        self.filename = "scores.csv"

        self.difficulty_x = {
            1: 1, # Grille facile
            2: 2, # Grille normale
            3: 3, # Grille difficile
            4: 4  # Grille expert
        }

        print("ScoreManager initialisé")


    def calculate_score(self, difficulty, moves): 

        multiplier = self.difficulty_x.get(difficulty, 1)

        score = multiplier * (100 - moves)

        # Validation que score n'est pas negatif
        if score < 0:
            score = 0

        return score

    # Test
if __name__ == "__main__":

    manager = ScoreManager()


score1 = manager.calculate_score(4, 20)
print(f"Pierre(exp, 20 coups) : {score1} pts")  

score2 = manager.calculate_score(2, 18)
print(f"Marie(nomal, 18 coups) : {score2} pts")  

