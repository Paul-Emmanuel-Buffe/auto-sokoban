# Auto-Sokoban 🎮🤖

Auto-Sokoban est un projet académique combinant développement de jeu et intelligence artificielle.  
L'objectif est de créer une version jouable du célèbre puzzle Sokoban avec un système de résolution automatique intégré.  

Le Sokoban est un jeu de réflexion où le joueur doit pousser des caisses vers des emplacements cibles dans un entrepôt, sans pouvoir les tirer.  
La difficulté réside dans la planification des mouvements pour éviter de bloquer les caisses.

---

## Fonctionnalités principales

### Partie 1 : Jeu interactif

- **Interface graphique** : développée avec Pygame.  
- **Représentation matricielle** : grille de jeu optimisée pour les calculs.  
- **Contrôles intuitifs** : 
  - Déplacements avec les flèches directionnelles.  
  - Annulation du dernier coup (`U`) et réinitialisation (`R`).  
  - Quitter avec `ESC`.  
- **Système de score** : sauvegarde dans une base de données SQLite pour suivre les performances.  
- **Niveaux multiples** : progression avec difficulté croissante.  
- **Éléments audiovisuels** : musique d'ambiance et effets sonores immersifs.

### Partie 2 : Intelligence artificielle

- **Solveur automatique avec BFS (Breadth-First Search)** : 
  - Résolution optimale en minimisant les mouvements.  
  - Exploration exhaustive garantissant la meilleure solution possible.  
- **Algorithme alternatif DFS (Depth-First Search)** : pour explorer des chemins profonds.  
- **Mode Hint (Indice)** : propose le prochain coup optimal pour guider le joueur.  
- **Visualisation** : affichage pas à pas de la solution calculée par l'IA.

---

## Méthodes employées

### Architecture logicielle

- **Séparation des responsabilités** : 
  - Logique métier.  
  - Gestion de l'affichage.  
  - Point d'entrée principal.  
- **Programmation orientée objet (POO)** : gestion des entités du jeu et interactions.  
- **Patterns de conception** : organisation propre et extensible du code.

### Algorithmes de résolution

- **Modélisation en graphe** : chaque état du jeu correspond à un nœud.  
- **Optimisations** : 
  - Élagage des états déjà visités pour éviter les cycles.  
  - Détection des blocages pour exclure les impasses.  
- **Exploration avec BFS** : garantit une solution optimale en parcourant les niveaux.  
- **Alternative DFS** : moins efficace, mais utile pour certaines analyses spécifiques.

### Technologies utilisées

- **Python** : langage principal pour la logique du jeu et les algorithmes.  
- **Pygame** : bibliothèque pour l'interface graphique et la gestion des événements.  
- **SQLite** : base de données légère pour la persistance des scores.  
- **Structures de données optimisées** : matrices, listes, dictionnaires pour garantir efficacité et clarté.

---

## Lancement du projet

### Prérequis

- **Python 3.x**  
- **Pygame** : `pip install pygame`  
- **Autres dépendances** : toutes listées dans `requirements.txt`.

### Instructions

1. Clonez le dépôt :
   ```bash
   git clone <URL_DU_DEPOT>
   cd Sokoban-Auto-Solver
