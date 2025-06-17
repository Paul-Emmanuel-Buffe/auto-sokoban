from build import *

def main():
    run = True
    games = Build_games()
    games.display_grid()
    while run:
        run = games.move()

if __name__ == "__main__":
    main()