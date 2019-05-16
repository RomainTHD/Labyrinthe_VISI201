"""
Algorithme "Randomized Kruskal's algorithm" (Fusion aléatoire de chemins).
"""

if __name__ == "__main__":
    raise ImportError("Executez ../main.py")

from environment.union_find import UnionFind
from environment.stack import Stack
from environment.position import Position
from environment.map import Map
from environment.direction import Direction

from generation.generic_generation import GenericGeneration

import random
import math

class Generation(GenericGeneration):
    def __init__(self):
        super().__init__("Randomized Kruskal's algorithm")

    def init(self):
        all_walls = []
        id_map = []

        for x, y in Map.dimensions:
            p = Position((x, y))

            id_map.append(p)

            if Map.isCellPosValid(p + Direction.RIGHT):
                all_walls.append((p, Direction.RIGHT))

            if Map.isCellPosValid(p + Direction.DOWN):
                all_walls.append((p, Direction.DOWN))

        random.shuffle(all_walls)
        self.all_walls = Stack(*all_walls)

        self.id_map = UnionFind(*id_map)

        self.old_p_wall = None

    def applyAlgorith(self):
        if self.old_p_wall is not None:
            Map.setWall(self.old_p_wall, Map.EMPTY)

        self.p1, dir = self.all_walls.pop()

        self.p_wall = self.p1 + dir/2

        p2 = self.p1 + dir

        self.can_draw = False

        repr_p1 = self.id_map.find(self.p1)
        repr_p2 = self.id_map.find(p2)

        if repr_p1 != repr_p2:
            self.can_draw = True

            self.id_map.union(self.p1, p2)

            self.old_p_wall = self.p_wall

            self.edited_wall_count += 1

    def drawPath(self):
        if self.slow:
            Map.setCell(self.p1, Map.YELLOW_CELL)

            if self.can_draw:
                Map.setWall(self.p_wall, Map.RED_WALL)

        if self.finished:
            Map.setWall(self.old_p_wall, Map.EMPTY)

    @staticmethod
    def getRandomDirection(p:Position) -> (Direction, None):
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

                """
                if visited_pos[new_p.x][new_p.y] is None:
                    # Si cette nouvelle case n'a jamais été visitée

                    if Map.getWall(p + dir/2) == Map.WALL:
                        # S'il y a bien un mur à briser

                        res = dir
                """

                if Map.getWall(p + dir/2) == Map.WALL:
                    # S'il y a bien un mur à briser

                    res = dir

        return res

    @staticmethod
    def displayIdMapAsText(id_map:list, frame_count:int) -> None:
        """
        Procédure affichant la liste des identifiants de façon lisible.

        INPUT :
            id_map : list list int, liste à 2 dimensions contenant les identifiants
                     entiers

        OUTPUT :
            None
        """

        raise NotImplementedError("Pas mis à jour")

        print("\nTableau des identifiants, frame : ",
              frame_count,
              "/",
              Map.width*Map.height-1,
              sep='')

        max_len = len(str(Map.width*Map.height))
        # Pour avoir des identifiants de même taille

        for x, y in Map.dimensions:
            if y == 0 and x != 0:
                print()

            s = id_map[x][y].strPos(1)

            while len(s) < max_len:
                s = '0' + s

            print(s, end=' ')

        print()
