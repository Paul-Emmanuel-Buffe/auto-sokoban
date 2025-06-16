# Auto-Sokoban 🎮🤖

## Contexte du projet
Auto-Sokoban est un projet académique combinant développement de jeu et intelligence artificielle. L'objectif est de créer une version jouable du célèbre puzzle Sokoban avec un système de résolution automatique intégré.
Le Sokoban est un jeu de réflexion où le joueur doit pousser des caisses vers des emplacements cibles dans un entrepôt, sans pouvoir les tirer. La difficulté réside dans la planification des mouvements pour éviter de bloquer les caisses.
Solution développée

## Partie 1 : Jeu interactif

Interface graphique développée avec Pygame
Représentation matricielle de la grille de jeu
Contrôles intuitifs avec les flèches directionnelles
Fonctionnalités avancées : annulation, réinitialisation, niveaux multiples
Système de score avec sauvegarde en base de données
Éléments audiovisuels : musique et effets sonores

## Partie 2 : Intelligence artificielle

Algorithmes de recherche BFS (Breadth-First Search) et DFS (Depth-First Search)
Résolution optimale en nombre minimal de mouvements
Visualisation pas à pas de la solution proposée par l'IA
Analyse des chemins et identification automatique des déplacements possibles

## Méthodes employées

### Architecture logicielle

Séparation des responsabilités : logique métier, affichage, et point d'entrée distincts
Programmation orientée objet pour la gestion des entités du jeu
Patterns de conception pour l'organisation du code

### Algorithmes de résolution

Modélisation en graphe : chaque état du jeu représente un nœud
Exploration exhaustive avec BFS pour garantir la solution optimale
Optimisations : élagage des états déjà visités, détection des blocages

### Technologies utilisées

Python : langage principal pour la logique et les algorithmes
Pygame : bibliothèque pour l'interface graphique et la gestion des événements
SQLite : base de données légère pour la persistance des scores
Structures de données : matrices, listes, dictionnaires pour l'efficacité
