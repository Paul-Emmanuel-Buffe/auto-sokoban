import pygame
import sys
from display_game import SokobanDisplay

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Menu Sokoban")
    font = pygame.font.Font(None, 36)
    
    def show_menu():
        while True:
            screen.fill((0, 0, 0))
            title = font.render("SOKOBAN", True, (255, 255, 255))
            start = font.render("1. Nouvelle partie", True, (255, 255, 255))
            quit = font.render("2. Quitter", True, (255, 255, 255))
            
            screen.blit(title, (200 - title.get_width()//2, 50))
            screen.blit(start, (200 - start.get_width()//2, 150))
            screen.blit(quit, (200 - quit.get_width()//2, 200))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        pygame.quit()
                        sys.exit()

    def choose_difficulty():
        # ... (identique à votre version précédente)
        return 1  # Par défaut
    
    while True:
        choice = show_menu()
        if choice == 1:
            difficulty = choose_difficulty()
            pygame.quit()  # Ferme le menu
            
            # Lance le jeu
            game = SokobanDisplay()
            game.setup_game(difficulty)
            game.run()
            
            # Après la partie, réinitialise
            pygame.init()
            screen = pygame.display.set_mode((400, 300))

if __name__ == "__main__":
    main()