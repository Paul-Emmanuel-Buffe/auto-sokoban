import csv
import os

# Classe de gestion du scoreboard
class ScoreManager:
    def __init__(self):
        
        self.filename = os.path.join(os.path.dirname(__file__), "scores.csv")


        self.difficulty_x = {
            1: 1, # Grille facile
            2: 2, # Grille normale
            3: 3, # Grille difficile
            4: 4  # Grille expert
        }

        self._create_file_not_exists()

        print("ScoreManager initialisé")

    def _create_file_not_exists(self):
        
        # Vérif de l'existence du csv
        if not os.path.exists(self.filename):
            print(f"Création csv {self.filename} !")

            # Création du csv si absent
            with open(self.filename, 'w', newline= '', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(["Nom", "Points"])

                print(f"Fichier {self.filename} créé avec succés !")
        else:
            print(f" Fichier {self.filename} trouvé ! ") 



    def save_score(self, player_name, difficulty, moves):
        score = self.calculate_score(difficulty, moves)
        joueur_found = False

        # Lecture du fichier, sauf la première ligne (en-tête)
        with open(self.filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)         # lire et stocker l'en-tête
            lignes = list(reader)         # lire uniquement les données

        # Update du score si joueur déjà présent
        for i in range(len(lignes)):
            nom, points = lignes[i]
            if nom == player_name:
                new_total = int(points) + score
                lignes[i] = [player_name, new_total]
                joueur_found = True
                break

        # Création si joueur absent
        if not joueur_found:
            lignes.append([player_name, score])


        # Tri des lignes par score décroissant (seule modification majeure)
            lignes.sort(key=lambda x: int(x[1]), reverse=True)

        # Ecriture du fichier : écriture de l'en-tête + données (sans doublons)
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Points'])  # Écrire une seule fois l'en-tête avec majuscule
            writer.writerows(lignes)             # écrire uniquement les données

        print(f"{player_name} -> {score} pts enregistrés")

              

    def calculate_score(self, difficulty, moves): 

        multiplier = self.difficulty_x.get(difficulty, 1)

        score = multiplier * (100 - moves)

        # Validation que score n'est pas negatif
        if score < 0:
            score = 0

        return score
    
    def get_scores(self):
        """Récupère la liste des scores triés par ordre décroissant"""
        scores = []
        
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Passe l'en-tête
                
                for row in reader:
                    if len(row) >= 2:  # Vérification que la ligne a au moins 2 colonnes
                        nom = row[0]
                        points = int(row[1])
                        scores.append((nom, points))
                        
        except FileNotFoundError:
            print(f"Fichier {self.filename} non trouvé")
        except Exception as e:
            print(f"Erreur lors de la lecture des scores: {e}")
        
        return scores

    # Test
# TEST DE L'ÉTAPE 2 - À exécuter pour vérifier
if __name__ == "__main__":
    print("=== TEST ETAPE 2 ===")
    
    # Crée un gestionnaire de scores
    manager = ScoreManager()
    
    print("\n--- Test de calcul (comme étape 1) ---")
    # Test du calcul (comme étape 1)
    score1 = manager.calculate_score(4, 20)  # Expert, 20 coups
    score2 = manager.calculate_score(2, 18)  # Normal, 18 coups
    print(f"Pierre (Expert, 20 coups) : {score1} points")
    print(f"Marie (Normal, 18 coups) : {score2} points")
    
    print("\n--- Test de sauvegarde ---")
    # NOUVEAU : Test de sauvegarde
    print("Sauvegarde de quelques scores de test...")
    
    manager.save_score("Pierre", 4, 20)  # Expert, 20 coups
    manager.save_score("Marie", 2, 18)   # Normal, 18 coups
    manager.save_score("Jean", 1, 15)    # Facile, 15 coups
    manager.save_score("Pierre", 3, 25)  # Pierre rejoue en Difficile
    
    print("\n✅ Vérifie maintenant le fichier 'scores.csv' dans ton dossier !")
    print("Tu devrais voir 4 lignes de données + 1 ligne d'en-têtes")
    
    print("\n=== FIN TEST ETAPE 2 ===")

