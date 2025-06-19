import pygame
import sys
from display_game import SokobanDisplay

def show_main_menu(screen, font, small_font):
    while True:
        screen.fill((0, 0, 0))
        title = font.render("SOKOBAN", True, (255, 255, 255))
        new_game = font.render("1. Nouvelle partie", True, (255, 255, 255))
        quit_game = font.render("2. Quitter", True, (255, 255, 255))

        screen.blit(title, (200 - title.get_width()//2, 100))
        screen.blit(new_game, (200 - new_game.get_width()//2, 200))
        screen.blit(quit_game, (200 - quit_game.get_width()//2, 250))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return show_difficulty_menu(screen, font, small_font)
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

def show_difficulty_menu(screen, font, small_font):
    while True:
        screen.fill((0, 0, 0))
        title = font.render("CHOISIR LA DIFFICULTE", True, (255, 255, 255))
        screen.blit(title, (200 - title.get_width()//2, 100))

        options = [
            ("1. Facile", 1),
            ("2. Normal", 2),
            ("3. Difficile", 3),
            ("4. Expert", 4)
        ]

        for i, (text, _) in enumerate(options):
            rendered = small_font.render(text, True, (255, 255, 255))
            screen.blit(rendered, (200 - rendered.get_width()//2, 180 + i * 40))

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Sokoban Menu")
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    difficulty = show_main_menu(screen, font, small_font)
    if difficulty is not None:
        pygame.quit()
        game = SokobanDisplay()
        game.setup_game(difficulty=difficulty)
        game.run()
        # Après la partie, on relance le menu
        main()

if __name__ == "__main__":
    main()
