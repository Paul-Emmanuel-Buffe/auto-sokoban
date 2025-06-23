import pygame
import sys
from build import Build_games
from score_manager import ScoreManager

class SokobanDisplay:
    def __init__(self):
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
        self.score_manager = ScoreManager()
    
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
                        player_name = self.ask_player_name()
                        if player_name:
                            difficulty = self.show_difficulty_menu()
                            if difficulty:
                                return (player_name, difficulty)
                    elif event.key == pygame.K_2:
                        self.show_scoreboard()
                    elif event.key == pygame.K_3:
                        pygame.quit()
                        sys.exit()

    def ask_player_name(self):
        """Demande le nom du joueur avec une interface graphique harmonisée"""
        screen_width, screen_height = 500, 300
        name_screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Nom du Joueur")
        
        # Couleurs harmonisées
        bg_color = (22, 29, 41)
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        input_color = (55, 65, 85)
        
        # Polices
        title_font = pygame.font.SysFont("Arial", 28, bold=True)
        text_font = pygame.font.SysFont("Arial", 24)
        input_font = pygame.font.SysFont("Arial", 26)
        
        player_name = ""
        cursor_visible = True
        cursor_timer = 0
        
        while True:
            name_screen.fill(bg_color)
            
            # Carte principale
            card_rect = pygame.Rect(50, 70, 400, 160)
            pygame.draw.rect(name_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(name_screen, accent_color, card_rect, width=3, border_radius=12)
            
            # Titre
            title = title_font.render("ENTREZ VOTRE NOM", True, accent_color)
            name_screen.blit(title, (screen_width // 2 - title.get_width() // 2, 90))
            
            # Zone de saisie
            input_rect = pygame.Rect(70, 130, 360, 40)
            pygame.draw.rect(name_screen, input_color, input_rect, border_radius=6)
            pygame.draw.rect(name_screen, accent_color, input_rect, width=2, border_radius=6)
            
            # Texte saisi + curseur
            display_text = player_name
            if cursor_visible and len(player_name) < 15:
                display_text += "|"
            
            text_surface = input_font.render(display_text, True, text_color)
            name_screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 8))
            
            # Instructions
            instruction = text_font.render("ENTRÉE = Valider    ESC = Retour", True, accent_color)
            name_screen.blit(instruction, (screen_width // 2 - instruction.get_width() // 2, 190))
            
            # Gestion du curseur clignotant
            cursor_timer += 1
            if cursor_timer > 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name.strip():
                            return player_name.strip()
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 15 and event.unicode.isprintable():
                            player_name += event.unicode

    def show_difficulty_menu(self):
        """Affiche le menu de difficulté avec style harmonisé"""
        difficulty_screen = pygame.display.set_mode((500, 400))
        pygame.display.set_caption("Choisir la Difficulté")
        
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
            difficulty_screen.fill(bg_color)

            # Carte
            pygame.draw.rect(difficulty_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(difficulty_screen, accent_color, card_rect, width=3, border_radius=12)

            # Titre 
            title_font = pygame.font.SysFont("Arial", 26, bold=True)
            title = title_font.render("CHOISIR LA DIFFICULTÉ", True, accent_color)
            difficulty_screen.blit(title, (difficulty_screen.get_width() // 2 - title.get_width() // 2, 70))

            # Options
            for i, (text, _) in enumerate(options):
                rendered = option_font.render(text, True, text_color)
                difficulty_screen.blit(rendered, (
                    difficulty_screen.get_width() // 2 - rendered.get_width() // 2,
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
        
    def setup_game(self, difficulty=1, player_name="Joueur"):
        """Initialise le jeu avec la difficulté et le nom spécifiés"""
        print(f"Configuration du jeu - Joueur: {player_name}, Difficulté: {difficulty}")
        self.game = Build_games(difficulty=difficulty, player_name=player_name)
        
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
        """Affiche un tableau de scores avec instructions parfaitement alignées"""
        original_display = pygame.display.get_surface()
        original_size = original_display.get_size()
        
        score_screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Classement des Scores")

        # Polices
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        item_font = pygame.font.SysFont('Arial', 28)
        footer_font = pygame.font.SysFont('Arial', 22)

        # Couleurs
        bg_color = (22, 29, 41)
        card_color = (36, 45, 60)
        line_color = (55, 65, 85)
        primary_color = (82, 216, 217)
        text_color = (240, 240, 240)

        # Dimensions
        card_rect = pygame.Rect(50, 50, 500, 400)

        while True:
            score_screen.fill(bg_color)
            
            # Carte principale
            pygame.draw.rect(score_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(score_screen, primary_color, card_rect, 3, border_radius=12)

            # Titre
            title = title_font.render("CLASSEMENT", True, primary_color)
            score_screen.blit(title, (300 - title.get_width()//2, 70))

            # Séparateur
            pygame.draw.line(score_screen, primary_color, (100, 120), (500, 120), 2)

            # Scores
            scores = self.score_manager.get_scores()[:10]
            y_pos = 150

            for i, (name, score) in enumerate(scores):
                if i % 2 == 0:
                    line_rect = pygame.Rect(100, y_pos-5, 400, 40)
                    pygame.draw.rect(score_screen, line_color, line_rect, border_radius=6)

                bullet = item_font.render("•", True, primary_color)
                name_text = item_font.render(name, True, text_color)
                score_text = item_font.render(str(score), True, primary_color)

                score_screen.blit(bullet, (110, y_pos))
                score_screen.blit(name_text, (140, y_pos))
                score_screen.blit(score_text, (450 - score_text.get_width(), y_pos))

                y_pos += 45

            # Instructions
            footer_y = card_rect.bottom - 40
            footer = footer_font.render("ESPACE pour revenir au menu", True, primary_color)
            footer_x = card_rect.centerx - footer.get_width() // 2
            
            footer_bg = pygame.Rect(footer_x - 10, footer_y - 5, 
                                footer.get_width() + 20, footer.get_height() + 10)
            pygame.draw.rect(score_screen, card_color, footer_bg, border_radius=8)
            pygame.draw.rect(score_screen, primary_color, footer_bg, 2, border_radius=8)
            
            score_screen.blit(footer, (footer_x, footer_y))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.display.set_mode(original_size)
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
            
            if success and self.game.check_victory():
                self.show_victory()
                
        elif key == pygame.K_r:
            self.game.reset_game()
        elif key == pygame.K_u:
            self.game.undo_last_move()
        elif key == pygame.K_ESCAPE:
            return False
        
        return True
    
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
        self.score_manager.save_score(
            self.game.player_name,
            self.game.difficulty,
            self.game.get_moves_count()
        )

        bg_color = (22, 29, 41)
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)

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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return self.show_main_menu()
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
                    if not self.handle_key(event.key):
                        running = False
            
            self.draw_game()
            self.clock.tick(60)
        
        pygame.display.quit()
        return

    def start_game(self):
        """Méthode principale pour démarrer le jeu avec menu"""
        while True:
            result = self.show_main_menu()
            if result is not None:
                player_name, difficulty = result
                self.setup_game(difficulty=difficulty, player_name=player_name)
                self.run()
            else:
                break

if __name__ == "__main__":
    game = SokobanDisplay()
    game.start_game()