try:
    from environment.position import *
except ImportError:
    from position import *

import random

class Direction(Position):
    """
    Classe contenant différentes directions héritant de la classe Position.

    Cette classe Direction a 4 variables statiques (les 4 directions) qui sont
    des instances de Direction.
    """

    all_directions = tuple()
    # Le tuple contenant toutes les directions. Est vide à l'origine

    @staticmethod
    def getRandomDirectionList() -> list:
        """
        Fonction retournant la liste des directions, triée de façon aléatoire.

        INPUT :
            None

        OUTPUT :
            dir_as_list : list Direction, liste des 4 directions
        """

        dir_as_list = list(Direction.all_directions)
        # On fait une copie du tuple de base en liste (modifiable)

        random.shuffle(dir_as_list)
        # On randomise la liste

        return dir_as_list

    def __init__(self, pos:Position, str_direction:str) -> None:
        """
        Fonction utilisée pour la création d'un objet direction.

        INPUT :
            pos : Position, la position (ex : (1, 0)) de la direction
            str_direction : str, le nom de la direction
        """

        super().__init__(pos)
        # Constructeur de la classe mère

        self.str_direction = str_direction

        self.opposite = None
        # Chaque direcion aura une direction opposée

        Direction.all_directions = Direction.all_directions + (self,)
        # On ajoute cette direction au tuple de toutes les directions

    def __str__(self) -> str:
        return self.str_direction

    def __repr__(self) -> str:
        return self.__str__()

Direction.RIGHT = Direction(( 1,  0), 'R')
Direction.DOWN  = Direction(( 0,  1), 'D')
Direction.LEFT  = Direction((-1,  0), 'L')
Direction.UP    = Direction(( 0, -1), 'U')

Direction.RIGHT.opposite = Direction.LEFT
Direction.UP.opposite    = Direction.DOWN
Direction.LEFT.opposite  = Direction.RIGHT
Direction.DOWN.opposite  = Direction.UP
