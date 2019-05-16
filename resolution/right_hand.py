"""
Algorithme "Right hand rule" (la règle de la main droite).
Le programme suit les murs de la main droite.
"""

if __name__ == "__main__":
    raise ImportError("Executez ../main.py")

from resolution.generic_resolution import GenericResolution

from environment.direction import Direction
from environment.map import Map
from environment.position import Position
import random
import time

class Resolution(GenericResolution):
    def __init__(self):
        super().__init__("Right hand rule")

    def init(self):
        self.new_p = Position(Map.start_pos)

        self.dir_id = 0
        self.increment_direction_id = 1
        # Mettre à 3 pour avoir la main gauche
        self.old_p = Position(self.new_p)

        self.nb_iter = 0

    def applyAlgorith(self):
        left_dir  = Direction.all_directions[(self.dir_id + self.increment_direction_id)%4]
        front_dir = Direction.all_directions[self.dir_id%4]

        self.move_forward = True

        if Map.isWallPosValid(self.new_p + left_dir/2) and Map.getWall(self.new_p + left_dir/2) == Map.EMPTY:
            # Si le mur de droite est valide et est vide...

            self.dir_id += self.increment_direction_id
            # On tourne dans la direction choisie
        elif not Map.isCellPosValid(self.new_p + front_dir) or Map.getWall(self.new_p + front_dir/2) == Map.WALL:
            # Sinon si la case devant est hors du plateau ou il y a un mur en face...

            self.dir_id += (self.increment_direction_id+2)%4
            # On tourne dans la direction opposée

            self.move_forward = False

        left_dir  = Direction.all_directions[(self.dir_id + self.increment_direction_id)%4]
        front_dir = Direction.all_directions[self.dir_id%4]
        # On recalcule les directions

        if self.move_forward:
            # S'il faut avancer on avance
            self.old_p = Position(self.new_p)
            self.new_p = self.new_p + front_dir
            self.go_forward_frame += 1

        self.nb_iter += 1

        if self.nb_iter == 4*Map.width*Map.height:
            raise GenericResolution.NoSolutionError()

    def drawPath(self):
        if self.slow:
            self.current_state = Map.getCell(self.new_p)
            Map.setCell(self.new_p, Map.ORANGE_CELL)

        if self.slow:
            Map.setCell(self.new_p, self.current_state)

        if self.move_forward:
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
        if self.new_p == Map.goal_pos:
            self.finished = True

            Map.setCell(self.old_p, Map.SOLUTION_PATH)
