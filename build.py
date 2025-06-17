from grid import *
class Build_games:
    def __init__(self):
        self.enter_name()
        self.choice_difficulty()
        self.placement = self.find_player()
        self.back_move = []

    
    def enter_name(self):
        self.player_name = input("please enter your name : ")

    def choice_difficulty(self):
        print("""level difficulty : 
            1 = easy
            2= normal
            3= hard
            """)
        while True:
            try:
                choice = int(input("choose a difficulty : "))
                
                if choice == 1:
                    print(f"you choose easy mode {self.player_name}")
                    self.grid = [list(row) for row in easy_grid ]
                elif choice == 2:
                    print(f"you choose normal mode {self.player_name}")
                    self.grid = [list(row) for row in normal_grid ]
                elif choice == 3:
                    print(f"you choose hard mode {self.player_name}")
                    self.grid = [list(row) for row in hard_grid ]
                else:
                    print("Invalid choice, please try again.")
                    continue 

            
                self.target_positions = [(i, j) for i, row in enumerate(self.grid)
                                        for j, cell in enumerate(row) if cell == "o"]

                return self.grid

            except ValueError:
                print("invalid value please choose another ")

    

    def display_grid(self):
        for i in self.grid:
            print("".join(i))      
    
    
    def find_player(self):
        for i, row in enumerate(self.grid):        
            for j, cell in enumerate(row):         
                if cell == "p":
                    self.player_i = i
                    self.player_j = j
                    return  (i, j) 
        
    def _update_cell(self, i, j):
        self.grid[i][j] = " "

    def move(self):
        move = input("Choisis un mouvement (z=haut, s=bas, q=gauche, d=droite): ").lower()
        delta = {
            "z": (-1, 0),
            "s": (1, 0),
            "q": (0, -1),
            "d": (0, 1)
        }

        if move not in delta:
            print("Commande invalide. Utilise z/s/q/d.")
            return

        di, dj = delta[move]
        i, j = self.player_i, self.player_j
        ni, nj = i + di, j + dj  

        
        if not (0 <= ni < len(self.grid) and 0 <= nj < len(self.grid[0])):
            print("Hors des limites.")
            return

        target = self.grid[ni][nj]

        
        if target in (" ", "o"):
            self._update_cell(i, j)
            self.grid[ni][nj] = "p"
            self.player_i, self.player_j = ni, nj
            self.back_move.append(move)

        
        elif target in ("b", "r"):  
            bi, bj = ni + di, nj + dj

            if not (0 <= bi < len(self.grid) and 0 <= bj < len(self.grid[0])):
                print("Impossible de pousser : hors limites.")
                return

            behind = self.grid[bi][bj]
            if behind in (" ", "o"):
                self.grid[bi][bj] = target
                self.grid[ni][nj] = "p"
                self._update_cell(i, j)
                self.player_i, self.player_j = ni, nj
                self.back_move.append(move)
                print(self.back_move)
            else:
                print("Impossible de pousser : obstacle derrière.")
        else:
            print("Tu ne peux pas aller là.")

        self.display_grid()

        if self.check_victory():
            print("🎉 Bravo ! Tous les blocs 'b' sont sur les cibles 'o' ! 🎉")
            return False
        return True


    def check_victory(self):
        for i, j in self.target_positions:
            if self.grid[i][j] != "b":
                return False
        return True

