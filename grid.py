# Grilles Sokoban corrigées et équilibrées

# FACILE : 2 caisses, 2 cibles - Apprentissage des mécaniques de base
easy_grid = [
    "#########",
    "#       #",
    "#   p   #",  # Joueur au centre-haut
    "#       #",
    "#  b b  #",  # Caisses au milieu
    "#       #",
    "# o   o #",  # Cibles en bas (joueur peut pousser vers le bas)
    "#       #",
    "#########"
]

# NORMAL : 3 caisses, 3 cibles - Nécessite de la planification
normal_grid = [
    "##########",
    "#        #",
    "#  o o o #",  # 3 cibles alignées
    "#        #",
    "####  ####",
    "#   ##   #",
    "#   p    #",  # Joueur avec espace de manœuvre
    "#   ##   #",
    "#  b b b #",  # 3 caisses à aligner avec les cibles
    "##########"
]

# DIFFICILE : 4 caisses, 4 cibles - Pattern complexe avec obstacles
hard_grid = [
    "############",
    "#    o  o  #",  # Cibles dans les coins
    "#          #",
    "#    ##    #",
    "# ## ## ## #",  # Obstacles créant des couloirs
    "#    ##    #",
    "#    p     #",  # Joueur au centre
    "#    ##    #",
    "# ## ## ## #",
    "#    ##    #",
    "#  b    b  #",  # Caisses à déplacer vers les cibles
    "#          #",
    "#  o    o  #",
    "############"
]

# BONUS : Grille très facile pour débuter (1 caisse, 1 cible)
tutorial_grid = [
    "#######",
    "#     #",
    "#  p  #",
    "#     #",
    "#  b  #",
    "#     #",
    "#  o  #",
    "#######"
]

# EXPERT : Pour les joueurs expérimentés (5 caisses, 5 cibles)
expert_grid = [
    "##############",
    "#  o  #  o   #",
    "#     #      #",
    "# ### # ###  #",
    "#     #   o  #",
    "####### ######",
    "#            #",
    "#     p      #",
    "#            #",
    "####### ######",
    "#  b  #   b  #",
    "#     #      #",
    "# ### # ###  #",
    "#  b  #  b   #",
    "# o   #      #",
    "##############"
]