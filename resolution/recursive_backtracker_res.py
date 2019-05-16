"""
Algorithme "Recursive backtracker" (exploration exhaustive).
"""

if __name__ == "_draw":
    raise ImportError("Executez ../main.py")

from resolution.generic_resolution import GenericResolution

from environment.map import *
from environment.direction import *
from environment.stack import *
import random
import time

class Resolution(GenericResolution):
    def __init__(self):
        super().__init__("Recursive backtracker res")

    def init(self):
        self.visited_pos = self.createList()
        # On crée la liste des positions visitées

        self.old_p = Position(Map.start_pos)

        self.new_p = Position(self.old_p)

        self.visited_pos_list = Stack()
        self.visited_pos_list.push(self.old_p)

        self.visited_pos[self.old_p.x][self.old_p.y] = True

        self.edited_wall_count = 0

    def applyAlgorith(self):
        self.dir = self.getRandomDirection(self.old_p, self.visited_pos)
        # On récupère une direction aléatoire

        if self.dir is None:
            if len(self.visited_pos_list) == 0:
                raise GenericResolution.NoSolutionError()

            self.old_p = self.visited_pos_list.pop()
            # Si aucune direction n'est libre, on remonte à la dernière position
        else:
            self.edited_wall_count += 1
            self.new_p = self.old_p + self.dir
            self.visited_pos[self.new_p.x][self.new_p.y] = True
            self.visited_pos_list.push(self.old_p)
            # On met à jour la liste des positions visitées

            self.go_forward_frame += 1

    def drawPath(self):
        if self.slow:
            # Si on prend notre temps pour dessiner à l'écran, on va
            # afficher une case orange à l'ancienne position

            self.etat = Map.getCell(self.old_p)

            Map.setCell(self.old_p, Map.ORANGE_CELL)

        if self.slow:
            Map.setCell(self.old_p, self.etat)
            # Maintenant qu'on a affiché la frame, on retire
            # la cellule orange

        if Map.getCell(self.new_p) == Map.EMPTY:
            Map.setCell(self.new_p, Map.SOLUTION_PATH)

            if self.old_p not in (Map.start_pos, Map.goal_pos):
                Map.setCell(self.old_p, Map.SOLUTION_PATH)
        elif Map.getCell(self.old_p) == Map.SOLUTION_PATH or Map.getCell(self.new_p) == Map.SOLUTION_PATH:
            if Map.getCell(self.new_p) not in (Map.START, Map.GOAL):
                Map.setCell(self.new_p, Map.VISITED_PATH)

                if self.old_p not in (Map.start_pos, Map.goal_pos):
                    Map.setCell(self.old_p, Map.VISITED_PATH)

    def checkIfFinished(self):
        if self.old_p == Map.goal_pos or self.new_p == Map.goal_pos:
            Map.setCell(self.old_p, Map.SOLUTION_PATH)
            self.finished = True

        if self.dir is not None:
            self.old_p = Position(self.new_p)
            # On met à jour la position

            if Map.isWallPosValid(self.new_p+self.dir/2):
                if Map.getWall(self.new_p+self.dir/2) == Map.EMPTY:
                    if self.new_p+self.dir == Map.goal_pos:
                        self.finished = True
            else:
                if self.old_p == Map.goal_pos:
                    self.finished = True

    @staticmethod
    def getRandomDirection(p:Position, visited_pos:list) -> (Direction, None):
        """
        Fonction permettant d'obtenir une direction aléatoire valide.

        INPUT :
            p : Position, une position
            visited_pos : list liste tuple, la liste des cases déjà visitées

        OUTPUT :
            res : Direction ou None si aucune direction n'est valide
        """

        list_dir = Direction.getRandomDirectionList()
        # On récupère les directions triées aléatoirement

        res = None

        for dir in list_dir:
            new_p = p + dir

            if Map.isCellPosValid(new_p):
                # Si la nouvelle case est bien dans le plateau

                if not visited_pos[new_p.x][new_p.y]:
                    # Si cette nouvelle case n'a jamais été visitée

                    if Map.getWall(p + dir/2) == Map.EMPTY:
                        # S'il n'y a pas de mur

                        res = dir

        return res

    @staticmethod
    def createList() -> list:
        """
        Fonction permettant de créer la liste des positions visitées.

        INPUT :
            None

        OUTPUT :
            visited_pos : list list tuple, tableau à 2 dimensions
                          des positions visitées
        """

        visited_pos = []

        for x in range(Map.width):
            # Création de la grille

            line = []

            for y in range(Map.height):
                line.append(False)

            visited_pos.append(line)

        return visited_pos
