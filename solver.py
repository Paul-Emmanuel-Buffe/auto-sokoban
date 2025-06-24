from collections import deque
import copy

class SokobanSolver:
    def __init__(self, grid, player_pos, targets):
        self.initial_grid = grid
        self.initial_player = player_pos
        self.targets = set(targets)
        self.rows = len(grid)
        self.cols = len(grid[0])

    def is_victory(self, boxes):
        """Vérifie si toutes les boîtes sont sur les cibles"""
        return all(pos in self.targets for pos in boxes)

    def serialize_state(self, player, boxes):
        """Encode un état pour l’éviter dans visited"""
        return (player, tuple(sorted(boxes)))

    def get_boxes(self, grid):
        """Retourne les positions de toutes les boîtes"""
        return {(i, j) for i, row in enumerate(grid)
                for j, val in enumerate(row) if val == 'b'}

    def is_free(self, grid, i, j, boxes):
        """Vérifie si une cellule est libre (pas un mur ni une boîte)"""
        return (0 <= i < self.rows and 0 <= j < self.cols and
                grid[i][j] != '#' and (i, j) not in boxes)

    def get_neighbors(self, player, boxes, grid):
        """Génère les états suivants valides"""
        directions = {'z': (-1, 0), 's': (1, 0), 'q': (0, -1), 'd': (0, 1)}
        neighbors = []

        for move, (di, dj) in directions.items():
            pi, pj = player
            ni, nj = pi + di, pj + dj

            if (ni, nj) in boxes:
                # Caisse devant → essayer de la pousser
                bi, bj = ni + di, nj + dj
                if self.is_free(grid, bi, bj, boxes):
                    new_boxes = set(boxes)
                    new_boxes.remove((ni, nj))
                    new_boxes.add((bi, bj))
                    neighbors.append(((ni, nj), new_boxes, move))
            elif self.is_free(grid, ni, nj, boxes):
                neighbors.append(((ni, nj), set(boxes), move))
        return neighbors

    def bfs(self):
        """Algorithme BFS pour résoudre le niveau"""
        initial_boxes = self.get_boxes(self.initial_grid)
        start = (self.initial_player, initial_boxes)
        visited = set()
        visited.add(self.serialize_state(*start))
        queue = deque([(start, [])])

        while queue:
            (player, boxes), path = queue.popleft()
            if self.is_victory(boxes):
                return path  # Retourne les mouvements

            for new_player, new_boxes, move in self.get_neighbors(player, boxes, self.initial_grid):
                state = self.serialize_state(new_player, new_boxes)
                if state not in visited:
                    visited.add(state)
                    queue.append(((new_player, new_boxes), path + [move]))
        return None

    def dfs(self, max_depth=1000):
        """Algorithme DFS pour résoudre le niveau (attention aux cycles)"""
        initial_boxes = self.get_boxes(self.initial_grid)
        start = (self.initial_player, initial_boxes)
        visited = set()
        visited.add(self.serialize_state(*start))
        stack = [(start, [])]

        while stack:
            (player, boxes), path = stack.pop()
            if len(path) > max_depth:
                continue
            if self.is_victory(boxes):
                return path

            for new_player, new_boxes, move in self.get_neighbors(player, boxes, self.initial_grid):
                state = self.serialize_state(new_player, new_boxes)
                if state not in visited:
                    visited.add(state)
                    stack.append(((new_player, new_boxes), path + [move]))
        return None

    def hint(self):
        """Retourne uniquement le premier coup optimal"""
        solution = self.bfs()
        if solution:
            return solution[0]  # Le premier coup conseillé
        return None
