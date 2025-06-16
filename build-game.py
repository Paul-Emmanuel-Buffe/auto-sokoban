from grid import *
class Build_games:
    def __init__(self):
        grid = self.choice_difficulty()

    def choice_difficulty(self):
        print("""level difficulty : 
              1 = easy
              2= normal
              3= hard
              """)
        choice = int(input("choose a difficulty : "))
        
        if choice == 1:
            print("easy")
            self.grid = grid_easy
        elif choice == 2:
            print("normal")
            self.grid = grid_normal
        elif choice != 1 and choice !=2:
            self.choice_difficulty()



    def display_grid(self):
        for i in self.grid:
            print(i)      
    
    
    
    def move(self):
        print("move")
    
    def backward_move(self):
        move_list = []


games = Build_games()

games.choice_difficulty()
games.display_grid()