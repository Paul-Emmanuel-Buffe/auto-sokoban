import sqlite3
import os

class ScoreManager:
    def __init__(self):
        # Chemin vers le fichier de base de données
        self.db_path = os.path.join(os.path.dirname(__file__), "scores.db")
        
        # Multiplicateurs de difficulté
        self.difficulty_multipliers = {
            1: 1,    # Facile
            2: 2,    # Normal
            3: 3,    # Difficile
            4: 4     # Expert
        }
        
        # Créer la table au démarrage
        self.create_table()

    def create_table(self):
        """Crée la table scores si elle n'existe pas"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Création de la table avec une requête SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                nom TEXT PRIMARY KEY,
                points INTEGER NOT NULL
            )
        ''')
        
        # Valider les changements et fermer la connexion
        conn.commit()
        conn.close()

    def save_score(self, player_name, difficulty, moves):
        """Enregistre ou met à jour le score d'un joueur"""
        # Calculer le nouveau score
        new_score = self.calculate_score(difficulty, moves)
        
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vérifier si le joueur existe déjà
        cursor.execute("SELECT points FROM scores WHERE nom = ?", (player_name,))
        result = cursor.fetchone()
        
        if result:
            # Le joueur existe : additionner les points
            total_points = result[0] + new_score
            cursor.execute("UPDATE scores SET points = ? WHERE nom = ?", 
                         (total_points, player_name))
        else:
            # Nouveau joueur : créer un enregistrement
            cursor.execute("INSERT INTO scores (nom, points) VALUES (?, ?)", 
                         (player_name, new_score))
        
        # Sauvegarder et fermer
        conn.commit()
        conn.close()

    def calculate_score(self, difficulty, moves):
        """Calcule le score avec le multiplicateur de difficulté"""
        multiplier = self.difficulty_multipliers.get(difficulty, 1)
        score = multiplier * (100 - moves)
        return max(score, 0)  # Le score ne peut pas être négatif

    def get_scores(self):
        """Retourne tous les scores triés du meilleur au moins bon"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Requête SQL pour récupérer les scores triés
        cursor.execute("SELECT nom, points FROM scores ORDER BY points DESC")
        scores = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()
        
        return scores

    def get_top_scores(self, limit=10):
        """Retourne les meilleurs scores (par défaut : top 10)"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Requête SQL avec LIMIT
        cursor.execute("SELECT nom, points FROM scores ORDER BY points DESC LIMIT ?", 
                      (limit,))
        scores = cursor.fetchall()
        
        conn.close()
        return scores

    def get_player_score(self, player_name):
        """Retourne le score d'un joueur spécifique"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Requête SQL pour un joueur spécifique
        cursor.execute("SELECT points FROM scores WHERE nom = ?", (player_name,))
        result = cursor.fetchone()
        
        conn.close()
        
        # Retourner le score ou 0 si le joueur n'existe pas
        if result:
            return result[0]
        else:
            return 0

    def delete_player(self, player_name):
        """Supprime un joueur de la base de données"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Requête SQL DELETE
        cursor.execute("DELETE FROM scores WHERE nom = ?", (player_name,))
        
        # Vérifier si une ligne a été supprimée
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted

    def count_players(self):
        """Retourne le nombre total de joueurs"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Requête SQL COUNT
        cursor.execute("SELECT COUNT(*) FROM scores")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count

    def reset_all_scores(self):
        """Supprime tous les scores de la base de données"""
        # Connexion à la base de données
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Requête SQL pour vider la table
        cursor.execute("DELETE FROM scores")
        
        conn.commit()
        conn.close()

    def print_scores(self):
        """Affiche tous les scores dans la console"""
        scores = self.get_scores()
        
        if not scores:
            print("Aucun score enregistré.")
            return
        
        print("=== CLASSEMENT ===")
        for i, (nom, points) in enumerate(scores, 1):
            print(f"{i}. {nom}: {points} points")


# Exemple d'utilisation simple
if __name__ == "__main__":
    # Créer le gestionnaire de scores
    manager = ScoreManager()
    
    print("=== TEST DU GESTIONNAIRE DE SCORES ===\n")
    
    # Ajouter quelques scores de test
    manager.save_score("Alice", 2, 25)    # Difficulté 2, 25 coups
    manager.save_score("Bob", 3, 30)      # Difficulté 3, 30 coups
    manager.save_score("Charlie", 1, 40)  # Difficulté 1, 40 coups
    manager.save_score("Alice", 1, 20)    # Alice rejoue
    
    # Afficher tous les scores
    manager.print_scores()
    
    # Afficher le top 3
    print("\n=== TOP 3 ===")
    top3 = manager.get_top_scores(3)
    for i, (nom, points) in enumerate(top3, 1):
        print(f"{i}. {nom}: {points} points")
    
    # Afficher le score d'un joueur spécifique
    alice_score = manager.get_player_score("Alice")
    print(f"\nScore d'Alice: {alice_score} points")
    
    # Afficher le nombre total de joueurs
    total_players = manager.count_players()
    print(f"Nombre total de joueurs: {total_players}")