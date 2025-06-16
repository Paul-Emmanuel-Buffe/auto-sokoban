from grid import *
class Build_games:
    def __init__(self):
        self.enter_name()
        self.choice_difficulty()
        self.placement = self.find_player()

    
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
                    return self.grid
                elif choice == 2:
                    print(f"you choose normal mode {self.player_name}")
                    self.grid = [list(row) for row in normal_grid ]
                    return self.grid
                elif choice == 3:
                    print(f"you choose hard mode {self.player_name}")
                    self.grid = [list(row) for row in hard_grid ]
                    return self.grid
                else:
                    print("Invalid choice, please try again.")
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
        
                
    def move(self):
        move =  input("choose where to move :").lower()
        
        if move == "u":
           self.grid[self.player_i][self.player_j] =" "
           self.grid[self.player_i - 1][self.player_j] = "p"
           self.player_i -= 1
           self.display_grid()
        if move == "d":
           self.grid[self.player_i][self.player_j] =" "
           self.grid[self.player_i + 1][self.player_j] = "p"
           self.player_i += 1
           self.display_grid()
        if move == "l":
           self.grid[self.player_i][self.player_j] =" "
           self.grid[self.player_i ][self.player_j -1] = "p"
           self.player_j -=1
           self.display_grid()
        if move == "r":
           self.grid[self.player_i][self.player_j] =" "
           self.grid[self.player_i][self.player_j + 1] = "p"
           self.player_j += 1
           self.display_grid()
         


    def backward_move(self):
        move_list = []


