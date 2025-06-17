from build import *

def main():
    run = True

    print("""
        1/ nouvelle partie
        2/ classement
        3/ quitter le jeu
        """)
    choice = int(input("veuillez choisir un des menu"))
    if choice == 1:
            games = Build_games()
            games.display_grid()
            while run:
                run = games.move()
    elif choice == 2:
            print("classement")
    elif choice == 3:
            run = False        

if __name__ == "__main__":
    main()