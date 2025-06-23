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
        """Affiche le menu principal avec un style moderne"""
        menu_screen = pygame.display.set_mode((500, 400))
        pygame.display.set_caption("Sokoban Menu")

        # Couleurs & police
        bg_color = (22, 29, 41)
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        title_font = pygame.font.SysFont("Arial", 42, bold=True)
        menu_font = pygame.font.SysFont("Arial", 28)

        while True:
            menu_screen.fill(bg_color)

            # Carte de menu
            card_rect = pygame.Rect(70, 50, 360, 300)
            pygame.draw.rect(menu_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(menu_screen, accent_color, card_rect, width=3, border_radius=12)

            # Titre
            title = title_font.render("SOKOBAN", True, accent_color)
            menu_screen.blit(title, (menu_screen.get_width() // 2 - title.get_width() // 2, 80))

            # Options
            options = [
                ("1. Nouvelle partie", pygame.K_1),
                ("2. Tableau des scores", pygame.K_2),
                ("3. Quitter", pygame.K_3)
            ]

            for i, (text, key) in enumerate(options):
                rendered = menu_font.render(text, True, text_color)
                y = 150 + i * 50
                menu_screen.blit(rendered, (menu_screen.get_width() // 2 - rendered.get_width() // 2, y))

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
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()



    def show_difficulty_menu(self, menu_screen):
        """Affiche le menu de difficulté avec style harmonisé"""
        # Couleurs
        bg_color = (22, 29, 41)
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        option_font = pygame.font.SysFont("Arial", 24)

        card_rect = pygame.Rect(70, 50, 360, 300)

        options = [
            ("1. Facile", 1),
            ("2. Normal", 2),
            ("3. Difficile", 3),
            ("4. Expert", 4)
        ]

        while True:
            menu_screen.fill(bg_color)

            # Carte
            pygame.draw.rect(menu_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(menu_screen, accent_color, card_rect, width=3, border_radius=12)

            # Titre 
            title_font = pygame.font.SysFont("Arial", 26, bold=True)
            title = title_font.render("CHOISIR LA DIFFICULTÉ", True, accent_color)
            menu_screen.blit(title, (menu_screen.get_width() // 2 - title.get_width() // 2, 70))


            # Options
            for i, (text, _) in enumerate(options):
                rendered = option_font.render(text, True, text_color)
                menu_screen.blit(rendered, (
                    menu_screen.get_width() // 2 - rendered.get_width() // 2,
                    140 + i * 40
                ))

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
        """Affiche un tableau de scores moderne, lisible et coloré"""
        screen_width, screen_height = 600, 500
        score_screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Classement des Scores")

        # Polices
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        item_font = pygame.font.SysFont('Arial', 28)
        footer_font = pygame.font.SysFont('Arial', 22)

        # Couleurs
        bg_color = (22, 29, 41)           # Fond général
        card_color = (36, 45, 60)         # Carte principale
        line_color = (55, 65, 85)         # Alternance ligne
        primary_color = (82, 216, 217)    # Turquoise clair
        text_color = (240, 240, 240)      # Texte blanc cassé

        # Dimensions carte
        card_rect = pygame.Rect(70, 50, 460, 380)

        while True:
            score_screen.fill(bg_color)

            # Carte principale
            pygame.draw.rect(score_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(score_screen, primary_color, card_rect, width=3, border_radius=12)

            # Titre (plus court et bien centré)
            title = title_font.render("SCORES", True, primary_color)
            score_screen.blit(title, (screen_width // 2 - title.get_width() // 2, 60))

            # Scores
            scores = self.score_manager.get_scores()[:10]
            y_pos = 130

            for i, (name, score) in enumerate(scores):
                line_rect = pygame.Rect(card_rect.x + 20, y_pos - 5, card_rect.width - 40, 38)
                if i % 2 == 0:
                    pygame.draw.rect(score_screen, line_color, line_rect, border_radius=6)

                bullet = item_font.render("•", True, primary_color)
                name_text = item_font.render(name, True, text_color)
                score_text = item_font.render(str(score), True, primary_color)

                score_screen.blit(bullet, (line_rect.x + 5, y_pos))
                score_screen.blit(name_text, (line_rect.x + 25, y_pos))
                score_screen.blit(score_text, (line_rect.right - score_text.get_width() - 10, y_pos))

                y_pos += 42

            # Footer
            footer = footer_font.render("Appuie sur ESPACE pour continuer", True, primary_color)
            score_screen.blit(footer, (
                screen_width // 2 - footer.get_width() // 2,
                card_rect.bottom - 30
            ))

            pygame.display.flip()

            # Événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
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
        """Affiche l'écran de victoire harmonisé graphiquement"""
        # Sauvegarde du score
        self.score_manager.save_score(
            self.game.player_name,
            self.game.difficulty,
            self.game.get_moves_count()
        )

        # Palette graphique
        bg_color = (22, 29, 41)
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)

        # Fonts
        title_font = pygame.font.SysFont("Arial", 36, bold=True)
        text_font = pygame.font.SysFont("Arial", 24)
        footer_font = pygame.font.SysFont("Arial", 20)

        screen_width, screen_height = self.screen.get_size()
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill(bg_color)
        self.screen.blit(overlay, (0, 0))

        # Carte
        card_rect = pygame.Rect(70, 100, screen_width - 140, 300)
        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=12)
        pygame.draw.rect(self.screen, accent_color, card_rect, width=3, border_radius=12)

        # Textes
        victory_text = title_font.render("🎉 VICTOIRE ! 🎉", True, accent_color)
        moves_text = text_font.render(f"Terminé en {self.game.get_moves_count()} coups !", True, text_color)
        replay_text = footer_font.render("ESPACE = menu principal    ESC = quitter", True, accent_color)

        self.screen.blit(victory_text, (screen_width // 2 - victory_text.get_width() // 2, 150))
        self.screen.blit(moves_text, (screen_width // 2 - moves_text.get_width() // 2, 210))
        self.screen.blit(replay_text, (screen_width // 2 - replay_text.get_width() // 2, 330))

        pygame.display.flip()

        # Attente input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return self.show_main_menu()  # Retour au menu principal
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    
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