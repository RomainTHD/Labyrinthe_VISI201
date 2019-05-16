from abc import ABC, abstractmethod
# Module pour avoir des méthodes abstraites

from environment.map import *
from environment.direction import *
from environment.settings import *
from environment.position import *

import random
import time

class GenericGeneration(ABC):
    def __init__(self, ALGORITHM_NAME):
        super().__init__()

        self.slow            = Settings.get("gen.slow", bool)
        self.start_in_corner = Settings.get("gen.start_in_corner", bool)
        self.end_in_corner   = Settings.get("gen.end_in_corner", bool)
        self.wall_ratio      = Settings.get("WALL_RATIO", float)

        self.ALGORITHM_NAME = ALGORITHM_NAME

    @abstractmethod
    def init(self):
        return

    @abstractmethod
    def applyAlgorith(self):
        pass

    @abstractmethod
    def drawPath(self):
        pass

    def start(self):
        print("Début de la génération :", self.ALGORITHM_NAME)

        self.finished = False
        self.edited_wall_count = 0
        self.total_frame_count = 0

        self.init()
        Map.syncModifiedCells()

        time_0 = time.time()

        ########################################################################

        while not self.finished:
            self.applyAlgorith()

            if self.edited_wall_count == Map.width*Map.height - 1:
                self.finished = True

            self.drawPath()

            self.total_frame_count += 1

            if self.slow:
                Map.syncModifiedCells()

            pourcentage = 100*self.edited_wall_count/(Map.width*Map.height - 1)
            pourcentage = int(10*pourcentage)/10

            print("Généré à {0}%".format(pourcentage), end='\r')

        if not self.slow:
            Map.syncModifiedCells()

        ########################################################################

        for x, y in Map.dimensions:
            # YELLOW_CELL
            Map.setCell((x, y), Map.EMPTY)

        if self.start_in_corner:
            Map.start_pos = Position((0, 0))
        else:
            Map.start_pos = Position.random((0, 0), (0, Map.height-1))

        if self.end_in_corner:
            Map.goal_pos = Position((Map.width-1, Map.height-1))
        else:
            Map.goal_pos = Position.random((Map.width-1, 0), (Map.width-1, Map.height-1))

        Map.setCell(Map.start_pos, Map.START)
        Map.setCell(Map.goal_pos, Map.GOAL)

        ########################################################################

        all_walls = []

        for x, y in Map.dimensions:
            p_horiz  = Position((x    , y+0.5))
            p_vertic = Position((x+0.5, y    ))

            if Map.isWallPosValid(p_horiz):
                if Map.getWall(p_horiz) == Map.WALL:
                    all_walls.append(p_horiz)

            if Map.isWallPosValid(p_vertic):
                if Map.getWall(p_vertic) == Map.WALL:
                    all_walls.append(p_vertic)

        random.shuffle(all_walls)

        walls_to_destroy = round(((Map.width-1)*(Map.height-1))*(100-self.wall_ratio)/100)
        all_walls = all_walls[:walls_to_destroy]

        for p in all_walls:
            Map.setWall(p, Map.EMPTY)

            if self.slow:
                Map.syncModifiedCells()

        if not self.slow:
            Map.syncModifiedCells()

        """
        all_walls = []

        for x, y in Map.dimensions:
            p_horiz  = Position((x    , y+0.5))
            p_vertic = Position((x+0.5, y    ))

            if Map.isWallPosValid(p_horiz):
                if Map.getWall(p_horiz) == Map.EMPTY:
                    all_walls.append(p_horiz)

            if Map.isWallPosValid(p_vertic):
                if Map.getWall(p_vertic) == Map.EMPTY:
                    all_walls.append(p_vertic)

        random.shuffle(all_walls)

        walls_to_destroy = round(((Map.width-1)*(Map.height-1))*(100-self.wall_ratio)/100)
        all_walls = all_walls[:walls_to_destroy]

        for p in all_walls:
            Map.setWall(p, Map.WALL)

            if self.slow:
                Map.syncModifiedCells()

        if not self.slow:
            Map.syncModifiedCells()
        """

        ########################################################################

        print("Génération terminée correctement")

        print("Nombre de tours théorique :", Map.width*Map.height - 1)
        print("Nombre de tours réel :", self.total_frame_count)

        try:
            efficiency = int(10*100 * self.edited_wall_count/self.total_frame_count)/10
        except ZeroDivisionError:
            efficiency = "NaN"

        print("Efficacité :", efficiency, "%")

        delta_t = int(10 * 1000 * (time.time()-time_0))/10
        print("Temps :", delta_t, "ms")

        print("Fin de la génération :", self.ALGORITHM_NAME)
