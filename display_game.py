import pygame
import sys
from build import Build_games
from score_manager import ScoreManager

class SokobanDisplay:
    def __init__(self):  # This line was incorrectly indented
        pygame.init()
        
        # Constantes
        self.CELL_SIZE = 50
        self.MARGIN = 50
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BROWN = (139, 69, 19)
        self.BLUE = (0, 0, 255)
        self.ORANGE = (255, 165, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        
        self.game = None
        self.screen = None
        self.score_manager = ScoreManager()  # <-- Ajout du gestionnaire de scores
    
    def show_main_menu(self):
        """Affiche le menu principal"""
        # Crée une fenêtre pour le menu
        menu_screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Sokoban Menu")
        
        while True:
            menu_screen.fill(self.BLACK)
            title = self.font.render("SOKOBAN", True, self.WHITE)
            new_game = self.font.render("1. Nouvelle partie", True, self.WHITE)
            scoreboard = self.font.render("2. Tableau des scores", True, self.WHITE)  # Nouvelle option
            quit_game = self.font.render("3. Quitter", True, self.WHITE)

        # Positions réorganisées (avec espacement)
            menu_screen.blit(title, (200 - title.get_width()//2, 100))
            menu_screen.blit(new_game, (200 - new_game.get_width()//2, 200))
            menu_screen.blit(scoreboard, (200 - scoreboard.get_width()//2, 250))  # Ligne ajoutée
            menu_screen.blit(quit_game, (200 - quit_game.get_width()//2, 300))  # Décalée vers le ba
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return self.show_difficulty_menu(menu_screen)
                    elif event.key == pygame.K_2:
                        self.show_scoreboard()
                    elif event.key == pygame.K_3:  # Décale la touche de sortie
                        pygame.quit()
                        sys.exit()

    def show_difficulty_menu(self, menu_screen):
        """Affiche le menu de sélection de difficulté"""
        while True:
            menu_screen.fill(self.BLACK)
            title = self.font.render("CHOISIR LA DIFFICULTE", True, self.WHITE)
            menu_screen.blit(title, (200 - title.get_width()//2, 100))

            options = [
                ("1. Facile", 1),
                ("2. Normal", 2),
                ("3. Difficile", 3),
                ("4. Expert", 4)
            ]

            for i, (text, _) in enumerate(options):
                rendered = self.small_font.render(text, True, self.WHITE)
                menu_screen.blit(rendered, (200 - rendered.get_width()//2, 180 + i * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_4:
                        return options[event.key - pygame.K_1][1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
        
    def setup_game(self, difficulty=1):
        """Initialise le jeu avec la difficulté spécifiée"""
        print(f"Configuration du jeu - Difficulté: {difficulty}")  # Debug
        self.game = Build_games(difficulty=difficulty, player_name="Joueur")
        
        # Vérification
        if not hasattr(self.game, 'grid'):
            raise ValueError("Erreur de chargement de la grille")
        
        # Calcul de la taille de la fenêtre
        rows = len(self.game.grid)
        cols = len(self.game.grid[0])
        width = cols * self.CELL_SIZE + 2 * self.MARGIN
        height = rows * self.CELL_SIZE + 2 * self.MARGIN + 100
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Sokoban - {self.game.get_difficulty_name()}")
    
    def draw_cell(self, x, y, cell_type):
        """Dessine une cellule selon son type"""
        rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
        
        # Fond de cellule
        pygame.draw.rect(self.screen, self.WHITE, rect)
        
        # Dessin des éléments
        if cell_type == '#':  # Mur
            pygame.draw.rect(self.screen, self.BROWN, rect)
        elif cell_type == 'p':  # Joueur
            pygame.draw.circle(self.screen, self.BLUE, 
                             (x + self.CELL_SIZE//2, y + self.CELL_SIZE//2), 
                             self.CELL_SIZE//3)
        elif cell_type == 'b':  # Caisse
            pygame.draw.rect(self.screen, self.ORANGE,
                            (x + 5, y + 5, self.CELL_SIZE - 10, self.CELL_SIZE - 10))
        elif cell_type == 'o':  # Cible
            pygame.draw.circle(self.screen, self.GREEN,
                             (x + self.CELL_SIZE//2, y + self.CELL_SIZE//2),
                             self.CELL_SIZE//4)
        elif cell_type == 'r':  # Obstacle
            pygame.draw.rect(self.screen, self.GRAY, rect)
        
        # Bordure
        pygame.draw.rect(self.screen, self.BLACK, rect, 2)
    

    def show_scoreboard(self):
        """Affiche le tableau des scores"""
        score_screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Tableau des Scores")
        
        while True:
            score_screen.fill(self.BLACK)
            
            # Titre
            title = self.font.render("TABLEAU DES SCORES", True, self.WHITE)
            score_screen.blit(title, (300 - title.get_width()//2, 50))
            
            # Récupère les scores
            try:
                scores = self.score_manager.get_scores()
            except:
                scores = []
                error_text = self.small_font.render("Erreur de chargement des scores", True, self.RED)
                score_screen.blit(error_text, (300 - error_text.get_width()//2, 120))
            
            # En-têtes
            header_name = self.small_font.render("Joueur", True, self.WHITE)
            header_score = self.small_font.render("Score", True, self.WHITE)
            score_screen.blit(header_name, (150, 120))
            score_screen.blit(header_score, (450, 120))
            
            # Affichage des scores (maximum 10)
            for i, (name, score) in enumerate(scores[:10]):
                name_text = self.small_font.render(name, True, self.WHITE)
                score_text = self.small_font.render(str(score), True, self.WHITE)
                score_screen.blit(name_text, (150, 150 + i * 30))
                score_screen.blit(score_text, (450, 150 + i * 30))
            
            # Instruction pour revenir
            back_text = self.small_font.render("Appuyez sur ESPACE pour revenir au menu", True, self.WHITE)
            score_screen.blit(back_text, (300 - back_text.get_width()//2, 450))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
    def draw_game(self):
        """Dessine tout le jeu"""
        self.screen.fill(self.WHITE)
        
        # Dessine la grille
        for i, row in enumerate(self.game.grid):
            for j, cell in enumerate(row):
                x = self.MARGIN + j * self.CELL_SIZE
                y = self.MARGIN + i * self.CELL_SIZE
                self.draw_cell(x, y, cell)
        
        # Informations en haut
        difficulty_text = self.small_font.render(f"Niveau: {self.game.get_difficulty_name()}", True, self.BLACK)
        moves_text = self.small_font.render(f"Coups: {self.game.get_moves_count()}", True, self.BLACK)
        player_text = self.small_font.render(f"Joueur: {self.game.player_name}", True, self.BLACK)
        controls_text = self.small_font.render("Flèches pour bouger, R=Reset, ESC=Quitter", True, self.BLACK)
        
        self.screen.blit(difficulty_text, (10, 10))
        self.screen.blit(moves_text, (10, 30))
        self.screen.blit(player_text, (10, 50))
        
        # Contrôles en bas
        screen_height = self.screen.get_height()
        self.screen.blit(controls_text, (10, screen_height - 30))
        
        pygame.display.flip()
    
    def handle_key(self, key):
        """Gère les touches du clavier"""
        move_map = {
            pygame.K_UP: 'z',
            pygame.K_DOWN: 's',
            pygame.K_LEFT: 'q',
            pygame.K_RIGHT: 'd'
        }
        
        if key in move_map:
            move = move_map[key]
            success = self.game.execute_move(move)
            
            # Vérifie la victoire après chaque mouvement réussi
            if success and self.game.check_victory():
                self.show_victory()
                
        elif key == pygame.K_r:
            # Reset du jeu
            self.game.reset_game()
        elif key == pygame.K_u:  # NOUVEAU: Touche U pour annuler
            # Annule le dernier mouvement
            self.game.undo_last_move()
        elif key == pygame.K_ESCAPE:
            return False  # Indique qu'on veut quitter
        
        return True  # Continue le jeu
    
    def draw_game(self):
            """Dessine tout le jeu"""
            self.screen.fill(self.WHITE)
            
            # Dessine la grille
            for i, row in enumerate(self.game.grid):
                for j, cell in enumerate(row):
                    x = self.MARGIN + j * self.CELL_SIZE
                    y = self.MARGIN + i * self.CELL_SIZE
                    self.draw_cell(x, y, cell)
            
            # Informations en haut
            difficulty_text = self.small_font.render(f"Niveau: {self.game.get_difficulty_name()}", True, self.BLACK)
            moves_text = self.small_font.render(f"Coups: {self.game.get_moves_count()}", True, self.BLACK)
            player_text = self.small_font.render(f"Joueur: {self.game.player_name}", True, self.BLACK)
            # MODIFIÉ: Ajout de la touche U dans les contrôles
            controls_text = self.small_font.render("Flèches=Bouger, U=Annuler, R=Reset, ESC=Quitter", True, self.BLACK)
            
            self.screen.blit(difficulty_text, (10, 10))
            self.screen.blit(moves_text, (10, 30))
            self.screen.blit(player_text, (10, 50))
            
            # Contrôles en bas
            screen_height = self.screen.get_height()
            self.screen.blit(controls_text, (10, screen_height - 30))
            
            pygame.display.flip()
    
    def show_victory(self):
        """Affiche l'écran de victoire"""
        victory_screen = pygame.Surface(self.screen.get_size())
        victory_screen.set_alpha(200)  # Semi-transparent
        victory_screen.fill(self.BLACK)

        # Sauvegarde du score
        self.score_manager.save_score(
            self.game.player_name,
            self.game.difficulty,
            self.game.get_moves_count()
        )
        
        victory_text = self.font.render("🎉 VICTOIRE! 🎉", True, self.WHITE)
        moves_text = self.small_font.render(f"Terminé en {self.game.get_moves_count()} coups!", True, self.WHITE)
        continue_text = self.small_font.render("Appuyez sur ESPACE pour rejouer ou ESC pour quitter", True, self.WHITE)
        
        # Centre les textes
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        victory_rect = victory_text.get_rect(center=(screen_width//2, screen_height//2 - 50))
        moves_rect = moves_text.get_rect(center=(screen_width//2, screen_height//2))
        continue_rect = continue_text.get_rect(center=(screen_width//2, screen_height//2 + 50))
        
        # Affiche l'écran de victoire
        self.screen.blit(victory_screen, (0, 0))
        self.screen.blit(victory_text, victory_rect)
        self.screen.blit(moves_text, moves_rect)
        self.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        
        # Attend une action du joueur
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Recommence le jeu
                        self.game.reset_game()
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Indique qu'on veut quitter
        
        return True  # Continue le jeu
    
    def run(self):
        """Boucle principale du jeu"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Gère les touches et vérifie si on doit quitter
                    if not self.handle_key(event.key):
                        running = False
            
            self.draw_game()
            self.clock.tick(60)
        
        # Nettoyage Pygame avant de retourner au menu
        pygame.display.quit()
        return  # Retourne au lieu de quitter complètement

    def start_game(self):
        """Méthode principale pour démarrer le jeu avec menu"""
        while True:
            difficulty = self.show_main_menu()
            if difficulty is not None:
                self.setup_game(difficulty=difficulty)
                self.run()
                # Après la partie, on retourne au menu principal
            else:
                break  # Si l'utilisateur ferme le jeu

# Pour tester directement
if __name__ == "__main__":
    game = SokobanDisplay()
    game.start_game()