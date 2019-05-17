from abc import ABC, abstractmethod
# Module pour avoir des méthodes abstraites

from environment.map import *
import time

class GenericResolution(ABC):
    class NoSolutionError(Exception):
        pass

    def __init__(self, ALGORITHM_NAME):
        super().__init__()

        self.slow = Settings.get("res.slow", bool)

        self.ALGORITHM_NAME = ALGORITHM_NAME

        self.happy_end = False
        self.finished = False
        self.total_frame_count = 0
        self.go_forward_frame = 0

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def applyAlgorith(self):
        pass

    @abstractmethod
    def drawPath(self):
        pass

    @abstractmethod
    def checkIfFinished(self):
        pass

    def start(self):
        print("Début de la résolution :", self.ALGORITHM_NAME)

        self.init()
        Map.syncModifiedCells()

        time_0 = time.time()

        while not self.finished:
            no_sol = False

            try:
                self.applyAlgorith()
            except GenericResolution.NoSolutionError:
                print("Pas de solution !")
                no_sol = True

            self.drawPath()
            self.checkIfFinished()

            if self.slow:
                Map.syncModifiedCells()

            if no_sol:
                self.finished = True

            self.total_frame_count += 1

        if not self.slow:
            Map.syncModifiedCells()

        """
        for x, y in Map.dimensions:
            if Map.getCell((x, y)) == Map.EMPTY:
                Map.setCell((x, y), Map.NOT_VISITED)

        Map.syncModifiedCells()
        """

        nb_solution_cell = 0
        nb_visited_cell = 0

        for x, y in Map.dimensions:
            etat = Map.getCell((x, y))

            if etat == Map.SOLUTION_PATH:
                nb_solution_cell += 1
            elif etat == Map.VISITED_PATH:
                nb_visited_cell += 1

        if no_sol:
            print("Résolution mal terminée")
        else:
            print("Résolution terminée correctement")

            print("Nombre de tours :", self.total_frame_count)

            print("Nombre de fois où l'algorithme a avancé :", self.go_forward_frame)

            print("Taille du chemin de solution :", nb_solution_cell, "cellules")
            print("Nombre total de cellules visitées :", nb_visited_cell + nb_solution_cell, "cellules")

            delta_t = int(10 * 1000 * (time.time()-time_0))/10
            print("Temps :", delta_t, "ms")

        print("Fin de la résolution :", self.ALGORITHM_NAME)
