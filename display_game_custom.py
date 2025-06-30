
import pygame
import sys
from build import Build_games
from score_manager import ScoreManager
from solver import SokobanSolver
import time

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
        self.ACCENT = (82, 216, 217)

        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()

        self.game = None
        self.screen = None
        self.score_manager = ScoreManager()

        # Chargement du background commun
        self.menu_background_raw = pygame.image.load("images/menu_background.png")
        self.menu_background = None  # sera converti après set_mode()

        # Boutons
        self.button_bfs = pygame.Rect(0, 0, 100, 40)
        self.button_dfs = pygame.Rect(0, 0, 100, 40)
        self.button_hint = pygame.Rect(0, 0, 100, 40)
        self.button_pause = pygame.Rect(0, 0, 100, 40)

        # Minuteur
        self.start_time = None
        self.elapsed_time = 0

        self.is_paused = False
        self.pause_start = None
        self.total_paused_time = 0

    def draw_background(self, surface):
        bg_scaled = pygame.transform.scale(self.menu_background, surface.get_size())
        surface.blit(bg_scaled, (0, 0))
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        surface.blit(overlay, (0, 0))

    def draw_button(self, surface, rect, text, font, active=False):
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        color = self.ACCENT if hover or active else self.GRAY
        shadow_rect = rect.copy()
        shadow_rect.move_ip(2, 2)
        pygame.draw.rect(surface, (20, 20, 20), shadow_rect, border_radius=8)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def show_scoreboard(self):
        original_display = pygame.display.get_surface()
        original_size = original_display.get_size()
        score_screen = pygame.display.set_mode((600, 500))
        self.menu_background = self.menu_background_raw.convert()
        pygame.display.set_caption("Classement des Scores")

        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        item_font = pygame.font.SysFont('Arial', 28)
        footer_font = pygame.font.SysFont('Arial', 22)

        card_color = (36, 45, 60)
        line_color = (55, 65, 85)
        primary_color = (82, 216, 217)
        text_color = (240, 240, 240)

        card_rect = pygame.Rect(50, 50, 500, 400)

        while True:
            self.draw_background(score_screen)

            pygame.draw.rect(score_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(score_screen, primary_color, card_rect, 3, border_radius=12)

            title = title_font.render("CLASSEMENT", True, primary_color)
            score_screen.blit(title, (300 - title.get_width()//2, 70))
            pygame.draw.line(score_screen, primary_color, (100, 120), (500, 120), 2)

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
    
    def show_welcome_screen(self):
        welcome_screen = pygame.display.set_mode((500, 400))
        self.menu_background = self.menu_background_raw.convert()
        pygame.display.set_caption("Welcome")

        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        title_font = pygame.font.SysFont("Arial", 42, bold=True)
        button_font = pygame.font.SysFont("Arial", 28)

        button_width, button_height = 160, 50
        button_rect = pygame.Rect(
            welcome_screen.get_width() // 2 - button_width // 2,
            welcome_screen.get_height() - button_height - 20,
            button_width,
            button_height
        )

        while True:
            self.draw_background(welcome_screen)

            self.draw_button(welcome_screen, button_rect, "PLAY", button_font)


            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return
            
    def show_main_menu(self):
        """Affiche le menu principal avec un style moderne"""
        self.cleanup_game()
        menu_screen = pygame.display.get_surface()  

        pygame.display.set_caption("Sokoban Menu")
        self.menu_background = self.menu_background_raw.convert()

        # Couleurs & police
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        title_font = pygame.font.SysFont("Arial", 42, bold=True)
        menu_font = pygame.font.SysFont("Arial", 28)

        options = [
            ("1. Nouvelle partie", pygame.K_1),
            ("2. Tableau des scores", pygame.K_2),
            ("3. Quitter", pygame.K_3)
        ]

        buttons = []
        for i in range(len(options)):
            rect = pygame.Rect(120, 150 + i * 60, 260, 45)
            buttons.append(rect)

        while True:
            bg_scaled = pygame.transform.scale(self.menu_background, menu_screen.get_size())
            menu_screen.blit(bg_scaled, (0, 0))
            overlay = pygame.Surface(menu_screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            menu_screen.blit(overlay, (0, 0))

            card_rect = pygame.Rect(70, 50, 360, 300)
            pygame.draw.rect(menu_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(menu_screen, accent_color, card_rect, width=3, border_radius=12)

            title = title_font.render("SOKOBAN", True, accent_color)
            menu_screen.blit(title, (menu_screen.get_width() // 2 - title.get_width() // 2, 80))

            for i, ((text, key), rect) in enumerate(zip(options, buttons)):
                self.draw_button(menu_screen, rect, text, menu_font)

            pygame.display.flip()
            self.clock.tick(60)  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(buttons):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                player_name = self.ask_player_name()
                                if player_name:
                                    difficulty = self.show_difficulty_menu()
                                    if difficulty:
                                        return (player_name, difficulty)
                            elif i == 1:
                                self.show_scoreboard()
                            elif i == 2:
                                pygame.quit()
                                sys.exit()

    def ask_player_name(self):
        """Demande le nom du joueur avec une interface graphique harmonisée"""
        screen_width, screen_height = 500, 300
        name_screen = pygame.display.get_surface()  
        pygame.display.set_caption("Nom du Joueur")

        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        input_color = (55, 65, 85)

        title_font = pygame.font.SysFont("Arial", 28, bold=True)
        text_font = pygame.font.SysFont("Arial", 24)
        input_font = pygame.font.SysFont("Arial", 26)

        player_name = ""
        cursor_visible = True
        cursor_timer = 0

        while True:
            bg_scaled = pygame.transform.scale(self.menu_background, name_screen.get_size())
            name_screen.blit(bg_scaled, (0, 0))

            card_rect = pygame.Rect(50, 70, 400, 160)
            pygame.draw.rect(name_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(name_screen, accent_color, card_rect, width=3, border_radius=12)

            title = title_font.render("ENTREZ VOTRE NOM", True, accent_color)
            name_screen.blit(title, (screen_width // 2 - title.get_width() // 2, 90))

            input_rect = pygame.Rect(70, 130, 360, 40)
            pygame.draw.rect(name_screen, input_color, input_rect, border_radius=6)
            pygame.draw.rect(name_screen, accent_color, input_rect, width=2, border_radius=6)

            display_text = player_name
            if cursor_visible and len(player_name) < 15:
                display_text += "|"

            text_surface = input_font.render(display_text, True, text_color)
            name_screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 8))

            instruction = text_font.render("ENTRÉE = Valider    ESC = Retour", True, accent_color)
            name_screen.blit(instruction, (screen_width // 2 - instruction.get_width() // 2, 190))

            cursor_timer += 1
            if cursor_timer > 30:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            pygame.display.flip()
            self.clock.tick(60)  

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
        difficulty_screen = pygame.display.get_surface()  
        pygame.display.set_caption("Choisir la Difficulté")
        self.menu_background = self.menu_background_raw.convert()

        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)
        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        option_font = pygame.font.SysFont("Arial", 24)

        options = [
            ("1. Facile", 1),
            ("2. Normal", 2),
            ("3. Difficile", 3),
            ("4. Expert", 4)
        ]

        buttons = []
        for i in range(len(options)):
            rect = pygame.Rect(120, 140 + i * 50, 260, 40)
            buttons.append(rect)

        while True:
            bg_scaled = pygame.transform.scale(self.menu_background, difficulty_screen.get_size())
            difficulty_screen.blit(bg_scaled, (0, 0))

            overlay = pygame.Surface(difficulty_screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            difficulty_screen.blit(overlay, (0, 0))

            card_rect = pygame.Rect(70, 50, 360, 300)
            pygame.draw.rect(difficulty_screen, card_color, card_rect, border_radius=12)
            pygame.draw.rect(difficulty_screen, accent_color, card_rect, width=3, border_radius=12)

            title = title_font.render("CHOISIR LA DIFFICULTÉ", True, accent_color)
            difficulty_screen.blit(title, (difficulty_screen.get_width() // 2 - title.get_width() // 2, 70))

            for i, ((text, val), rect) in enumerate(zip(options, buttons)):
                self.draw_button(difficulty_screen, rect, text, option_font)

            pygame.display.flip()
            self.clock.tick(60)  # ✅ Ajout essentiel

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_4:
                        return options[event.key - pygame.K_1][1]
                    elif event.key == pygame.K_ESCAPE:
                        return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(buttons):
                        if rect.collidepoint(event.pos):
                            return options[i][1]


    def setup_game(self, difficulty=1, player_name="Joueur"):
        """Initialise le jeu avec la difficulté et le nom spécifiés"""
        print(f"Configuration du jeu - Joueur: {player_name}, Difficulté: {difficulty}")
        
        # Nettoie complètement l'ancien jeu
        self.cleanup_game()
        # Initialise le temps de jeu
        self.start_time = time.time()

        
        # Crée toujours une nouvelle instance fraîche
        self.game = Build_games(difficulty=difficulty, player_name=player_name)
        
        # Vérification
        if not hasattr(self.game, 'grid'):
            raise ValueError("Erreur de chargement de la grille")
        
        # Recalcule toujours la taille de fenêtre
        rows = len(self.game.grid)
        cols = len(self.game.grid[0])
        width = cols * self.CELL_SIZE + 2 * self.MARGIN
        height = rows * self.CELL_SIZE + 2 * self.MARGIN + 100
        
        # Recrée la fenêtre avec la bonne taille
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Sokoban - {self.game.get_difficulty_name()}")
        
        print(f"Fenêtre créée: {width}x{height}")
    
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
    
    


    def handle_key(self, key):
        """Gère les touches du clavier"""
        pygame.mixer.init()

        sound_map = {
            pygame.K_UP: r"C:\Users\ndiay\Desktop\lptf\projets\IA\ALGO\sokoban\new\sounds\683245__saha213131__fart.mp3",
            pygame.K_DOWN: r"C:\Users\ndiay\Desktop\lptf\projets\IA\ALGO\sokoban\new\sounds\721355__bipolarbad__short-fart-again.mp3",
            pygame.K_LEFT: r"C:\Users\ndiay\Desktop\lptf\projets\IA\ALGO\sokoban\new\sounds\683245__saha213131__fart.mp3",
            pygame.K_RIGHT: r"C:\Users\ndiay\Desktop\lptf\projets\IA\ALGO\sokoban\new\sounds\721355__bipolarbad__short-fart-again.mp3",
            
        }
    
        if key in sound_map:
            sound = pygame.mixer.Sound(sound_map[key])
            sound.play()
    

        if self.is_paused:
            return True  # Ignore les touches en pause
        
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
                victory_result = self.show_victory()
                if victory_result == "menu":
                    return False  # Retourne False pour sortir de la boucle de jeu
                
        elif key == pygame.K_r:
            self.game.reset_game()
        elif key == pygame.K_u:
            self.game.undo_last_move()
        elif key == pygame.K_ESCAPE:
            return False
        
        return True
    
    def draw_game(self):
        self.draw_background(self.screen)
        card_color = (36, 45, 60)
        accent_color = (82, 216, 217)
        text_color = (240, 240, 240)

        font = pygame.font.SysFont("Arial", 24)
        small_font = pygame.font.SysFont("Arial", 20)

        rows = len(self.game.grid)
        cols = len(self.game.grid[0])
        grid_width = cols * self.CELL_SIZE
        grid_height = rows * self.CELL_SIZE
        card_padding = 20

        top_margin = 120
        card_rect = pygame.Rect(
            (self.screen.get_width() - grid_width) // 2 - card_padding,
            top_margin,
            grid_width + 2 * card_padding,
            grid_height + 2 * card_padding
        )

        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=12)
        pygame.draw.rect(self.screen, accent_color, card_rect, width=3, border_radius=12)

        start_x = card_rect.x + card_padding
        start_y = card_rect.y + card_padding
        for i, row in enumerate(self.game.grid):
            for j, cell in enumerate(row):
                x = start_x + j * self.CELL_SIZE
                y = start_y + i * self.CELL_SIZE
                self.draw_cell(x, y, cell)

        info_x = self.screen.get_width() - 600
        self.screen.blit(self.small_font.render(f"Niveau : {self.game.get_difficulty_name()}", True, text_color), (info_x, 10))
        self.screen.blit(self.small_font.render(f"Coups : {self.game.get_moves_count()}", True, text_color), (info_x, 40))
        self.screen.blit(self.small_font.render(f"Joueur : {self.game.player_name}", True, text_color), (info_x, 70))

        if self.start_time and not self.is_paused:
            current_time = time.time()
            self.elapsed_time = current_time - self.start_time - self.total_paused_time

        minutes = int(self.elapsed_time) // 60
        seconds = int(self.elapsed_time) % 60
        timer_text = self.small_font.render(f"Temps: {minutes:02d}:{seconds:02d}", True, text_color)
        self.screen.blit(timer_text, (self.screen.get_width() - 120, 10))

        if self.is_paused:
            pause_font = pygame.font.SysFont("Arial", 48, bold=True)
            pause_text = pause_font.render("PAUSE", True, accent_color)
            self.screen.blit(pause_text, (
                self.screen.get_width() // 2 - pause_text.get_width() // 2,
                self.screen.get_height() // 2 - pause_text.get_height() // 2
            ))

        top_buttons_y = 20
        spacing = 10
        total_width = 3 * self.button_bfs.width + 2 * spacing
        start_x = (self.screen.get_width() - total_width) // 2

        self.button_bfs.topleft = (start_x+15, top_buttons_y)
        self.button_dfs.topleft = (self.button_bfs.right + spacing, top_buttons_y)
        self.button_hint.topleft = (self.button_dfs.right + spacing, top_buttons_y)

        pause_x = (self.button_bfs.left + self.button_hint.right) // 2 - self.button_pause.width // 2
        pause_y = self.button_bfs.bottom + 10
        self.button_pause.topleft = (pause_x, pause_y)

        
        # Boutons avec icônes modernes
        self.draw_button(self.screen, self.button_bfs, " BFS", self.small_font)
        self.draw_button(self.screen, self.button_dfs, " DFS", self.small_font)
        self.draw_button(self.screen, self.button_hint, " Hint", self.small_font)

        # Bouton pause/reprise
        label = " Pause" if not self.is_paused else " play"
        self.draw_button(self.screen, self.button_pause, label, self.small_font)


        controls_text = small_font.render("Fl\u00e8ches = bouger    U = annuler    R = reset    ESC = quitter", True, accent_color)
        self.screen.blit(controls_text, (
            self.screen.get_width() // 2 - controls_text.get_width() // 2,
            self.screen.get_height() - 40
        ))

        pygame.display.flip()
    
    def cleanup_game(self):
        self.game = None
        self.screen = None
        pygame.display.set_mode((500, 400))
        
        
    def solve_with(self, method):
        self.solver = SokobanSolver(
            self.game.grid,
            (self.game.player_i, self.game.player_j),
            self.game.target_positions
        )
        path = self.solver.bfs() if method == 'bfs' else self.solver.dfs()
        if not path:
            print("Aucune solution trouvée.")
            return
        for move in path:
            pygame.time.delay(200)
            self.game.execute_move(move)
            self.draw_game()
            if self.game.check_victory():
                result = self.show_victory()
                if result == "menu":
                    return "menu"
                

    def give_hint(self):
        self.solver = SokobanSolver(
            self.game.grid,
            (self.game.player_i, self.game.player_j),
            self.game.target_positions
        )
        hint = self.solver.hint()
        if hint:
            self.game.execute_move(hint)
            if self.game.check_victory():
                self.show_victory()
                
    def show_victory(self):
        """Affiche l'écran de victoire harmonisé graphiquement"""
        
        pygame.mixer.init()
        sound = pygame.mixer.Sound(r"C:\Users\ndiay\Desktop\lptf\projets\IA\ALGO\sokoban\new\sounds\490248__abolla__fart-01.wav")
        sound.play()
        
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
                        # CORRECTION: Retourne directement au menu, ne pas relancer le jeu
                        return "menu"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.is_paused and not self.handle_key(event.key):
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.button_bfs.collidepoint(x, y):
                        result = self.solve_with('bfs')
                        if result == "menu":
                            running = False
                    elif self.button_dfs.collidepoint(x, y):
                        result = self.solve_with('dfs')
                        if result == "menu":
                            running = False
                    elif self.button_hint.collidepoint(x, y):
                        self.give_hint()

                    elif self.button_pause.collidepoint(event.pos):
                        if not self.is_paused:
                            self.is_paused = True
                            self.pause_start = time.time()
                        else:
                            self.is_paused = False
                            self.total_paused_time += time.time() - self.pause_start
            
            self.draw_game()
            self.clock.tick(60)

        self.cleanup_game()
        return


    def start_game(self):
        
        """Méthode principale pour démarrer le jeu avec menu"""
        pygame.display.set_mode((500, 400))  # ✅ Initialise le mode vidéo global
        self.menu_background = self.menu_background_raw.convert()  # ✅ Convert possible ici

        self.show_welcome_screen()  # écran de bienvenue en premier
        while True:
            result = self.show_main_menu()
            if result is not None:
                player_name, difficulty = result
                self.setup_game(difficulty=difficulty, player_name=player_name)
                self.run()
                self.cleanup_game()
            else:
                break


if __name__ == "__main__":
    game = SokobanDisplay()
    game.start_game()