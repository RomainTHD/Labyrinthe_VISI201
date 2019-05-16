"""
Algorithme "Recursive backtracker" (Exploration exhaustive).
"""

if __name__ == "__main__":
    raise ImportError("Executez ../main.py")

from environment.map import *
from environment.direction import *
from environment.stack import *

from generation.generic_generation import GenericGeneration

class Generation(GenericGeneration):
    def __init__(self):
        super().__init__("Recursive backtracker gen")

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

                    if Map.getWall(p + dir/2) == Map.WALL:
                        # S'il y a bien un mur à briser

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

    def init(self):
        self.visited_pos = self.createList()
        # On crée la liste des positions visitées

        self.old_p = Position.random((0, 0), (Map.width-1, Map.height-1))
        # La case d'origine est une case aléatoire

        if self.slow:
            Map.setCell(self.old_p, Map.YELLOW_CELL)

        self.visited_pos_list = Stack()
        self.visited_pos_list.push(self.old_p)

        self.visited_pos[self.old_p.x][self.old_p.y] = True

    def applyAlgorith(self):
        self.dir = self.getRandomDirection(self.old_p, self.visited_pos)
        # On récupère une direction aléatoire

        if self.dir is None:
            self.old_old_p = Position(self.old_p)
            self.new_p = self.visited_pos_list.pop()
            # Si aucune direction n'est libre, on remonte à la dernière position
        else:
            self.edited_wall_count += 1

            Map.setWall(self.old_p+self.dir/2, Map.EMPTY)
            # On affiche le mur brisé en rouge

            self.new_p = self.old_p + self.dir
            self.visited_pos[self.new_p.x][self.new_p.y] = True
            self.visited_pos_list.push(self.old_p)
            # On met à jour la liste des positions visitées

    def drawPath(self):
        if self.slow:
            Map.setCell(self.new_p, Map.ORANGE_CELL)
            Map.setCell(self.old_p, Map.YELLOW_CELL)

        self.old_p = Position(self.new_p)
        # On met à jour la position
