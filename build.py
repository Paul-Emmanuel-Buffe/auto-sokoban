from grid import *

class Build_games:
    def __init__(self, difficulty=1, player_name="Joueur"):  # Modification ici
        self.player_name = player_name  # Nouvelle ligne ajoutée
        self.difficulty = difficulty
        self.grid = []
        self.original_grid = None
        self.back_move = []
        self.target_positions = []  
        
        self.setup_grid()
        self.placement = self.find_player()

    def setup_grid(self):
        """Configure la grille selon la difficulté"""
        grid_map = {
            1: easy_grid,
            2: normal_grid,
            3: hard_grid,
            4: expert_grid
        }
        
        # Validation de la difficulté
        if self.difficulty not in grid_map:
            print(f"Difficulté {self.difficulty} invalide, utilisation du niveau Facile")
            self.difficulty = 1
        
        selected_grid = grid_map[self.difficulty]
        
        # Initialise self.grid AVANT de l'utiliser
        self.grid = [list(row) for row in selected_grid]
        
        # Sauvegarde pour le reset
        self.original_grid = [list(row) for row in selected_grid]
        
        # CORRECTION: Trouve les positions des cibles
        self.target_positions = [(i, j) for i, row in enumerate(self.grid)
                                for j, cell in enumerate(row) if cell == "o"]
        
        # Compte les caisses pour vérifier la cohérence
        box_count = sum(row.count('b') for row in self.grid)
        target_count = len(self.target_positions)
        
        print(f"Niveau {self.difficulty}: {box_count} caisses, {target_count} cibles")

    def find_player(self):
        """Trouve la position du joueur dans la grille"""
        for i, row in enumerate(self.grid):        
            for j, cell in enumerate(row):         
                if cell == "p":
                    self.player_i = i
                    self.player_j = j
                    return (i, j)
        return None
    
    def _update_cell(self, i, j):
        """Met à jour une cellule en la vidant"""
        # Vérifie si c'était une cible avant de la vider
        if (i, j) in self.target_positions:
            self.grid[i][j] = "o"  # Remet la cible
        else:
            self.grid[i][j] = " "  # Case vide
    
    def execute_move(self, move):
        """
        Exécute un mouvement donné
        move: 'z'=haut, 's'=bas, 'q'=gauche, 'd'=droite
        Retourne True si le mouvement a réussi
        """
        delta = {
            "z": (-1, 0),  # Haut
            "s": (1, 0),   # Bas
            "q": (0, -1),  # Gauche
            "d": (0, 1)    # Droite
        }
        
        if move not in delta:
            return False
        
        di, dj = delta[move]
        i, j = self.player_i, self.player_j
        ni, nj = i + di, j + dj  # Nouvelle position
        
        # Vérifie si on sort de la grille
        if not (0 <= ni < len(self.grid) and 0 <= nj < len(self.grid[0])):
            return False
        
        target = self.grid[ni][nj]  # Ce qu'il y a à la nouvelle position
        
        # Mouvement simple (case vide ou cible)
        if target in (" ", "o"):
            self._update_cell(i, j)  # Nettoie l'ancienne position
            self.grid[ni][nj] = "p"  # Place le joueur
            self.player_i, self.player_j = ni, nj  # Met à jour la position
            self.back_move.append(move)  # Enregistre le mouvement
            return True
        
        # Poussée de caisse (b) ou d'obstacle (r)
        elif target in ("b", "r"):  
            bi, bj = ni + di, nj + dj  # Position derrière la caisse
            
            # Vérifie si la position derrière sort de la grille
            if not (0 <= bi < len(self.grid) and 0 <= bj < len(self.grid[0])):
                return False
            
            behind = self.grid[bi][bj]  # Ce qu'il y a derrière la caisse
            
            # On peut pousser seulement sur case vide ou cible
            if behind in (" ", "o"):
                self.grid[bi][bj] = target  # Déplace la caisse
                self.grid[ni][nj] = "p"     # Place le joueur
                self._update_cell(i, j)     # Nettoie l'ancienne position
                self.player_i, self.player_j = ni, nj  # Met à jour la position
                self.back_move.append(move)  # Enregistre le mouvement
                return True
            else:
                return False  # Impossible de pousser
        
        # Mur ou autre obstacle
        else:
            return False
    
    def check_victory(self):
        """Vérifie si toutes les caisses sont sur les cibles"""
        for i, j in self.target_positions:
            if self.grid[i][j] != "b":  # Si pas de caisse sur cette cible
                return False
        return True
    
    def get_moves_count(self):
        """Retourne le nombre de mouvements effectués"""
        return len(self.back_move)
    
    def reset_game(self):
        """Remet le jeu à zéro"""
        if self.original_grid:
            self.grid = [list(row) for row in self.original_grid]
            self.find_player()
            self.back_move = []
    
    def get_difficulty_name(self):
        """Retourne le nom de la difficulté"""
        names = {
            0: "Tutorial",
            1: "Facile", 
            2: "Normal",
            3: "Difficile",
            4: "Expert"
        }
        return names.get(self.difficulty, "Inconnu")
    def undo_last_move(self):
        """Annule le dernier mouvement """
        if not self.back_move:
            return False  # Aucun mouvement à annuler
        
        # Méthode simple : on recharge la grille et on rejoue tous les mouvements sauf le dernier
        if len(self.back_move) == 1:
            # Si c'est le premier mouvement, on reset complètement
            self.reset_game()
            return True
        
        # Sauvegarde tous les mouvements sauf le dernier
        moves_to_replay = self.back_move[:-1]
        
        # Reset du jeu
        self.reset_game()
        
        # Rejoue tous les mouvements sauf le dernier
        for move in moves_to_replay:
            self.execute_move(move)
        
        return True