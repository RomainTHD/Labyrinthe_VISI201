try:
    from environment.direction import Direction
    from environment.position import Position
    from environment.settings import Settings
    from environment.queue import Queue
except ImportError:
    from direction import Direction
    from position import Position
    from settings import Settings
    from queue import Queue

class Map:
    """
    Classe représentant le labyrinthe / le plateau de jeu

    x x x x x x x x x x x
    x O - O - O - O - O x
    x | * | * | * | * | x
    x O - O - A B O - O x
    x | * | * C * | * | x
    x O - O - O - O - O x
    x | * | * | * | * | x
    x O - O - O - O - O x
    x | * | * | * | * | x
    x O - O - O - O - O x
    x x x x x x x x x x x

    Les 'O' sont des cases vides
    Les '─' et '|' sont des murs ou des portes
    Les '*' sont des intersections, qui ne peuvent pas être supprimées
    Les 'x' sont des murs extérieurs, qui ne peuvent pas non plus être supprimés

    'A' a pour position absolue (5, 3) mais on considère qu'elle est (2, 1)
    'B' a pour position absolue (6, 3) mais on considère qu'elle est (2.5, 1)
    'C' a pour position absolue (5, 4) mais on considère qu'elle est (2, 1.5)

    Chaque changement de cellule ou de mur est par défaut enregistré dans une Queue
    pour l'afficher a posteriori.
    """

    # Variables pour éviter l'utilisation de nombres magiques
    # et ainsi augmenter la lisibilité

    SET_TYPE_WALL = 11
    SET_TYPE_CELL = 12
    # Utilisé pour savoir si une case est modifiée comme mur ou cellule

    EMPTY = 21
    # Cellule ou mur vide

    WALL = 31
    RED_WALL = 32
    # Murs pleins. Un mur rouge est un mur plus (+) visible

    START = 41
    GOAL = 42
    # Repères pour savoir où sont le début et la fin du labyrinthe

    YELLOW_CELL = 51
    ORANGE_CELL = 52
    # Repères visuels décoratifs

    SOLUTION_PATH = 61
    VISITED_PATH = 62
    NOT_VISITED = 63
    # Pour la résolution

    @classmethod
    def resetAll(cls, save:bool) -> None:
        """
        Réinitialise la grille

        INPUT :
            save : bool, si cette réinitialisation doit être sauvegardée pour
                         l'affichage
        """

        for x, y in cls.dimensions:
            p_horiz  = Position((x    , y+0.5))
            p_vertic = Position((x+0.5, y    ))

            if cls.isWallPosValid(p_horiz):
                cls.setWall(p_horiz, cls.WALL, save=save)

            if Map.isWallPosValid(p_vertic):
                cls.setWall(p_vertic, cls.WALL, save=save)

            cls.setCell((x, y), cls.EMPTY, save=save)

    @classmethod
    def modifyCell(cls) -> bool:
        """
        Permet d'appliquer les modifications faites lors de la génération et de
        la résolution lors de l'affichage à l'écran

        OUTPUT :
            bool, si c'était la dernière modification ou non

        EXCEPTION :
            ValueError, si les types ne correspondent pas
        """

        if len(cls.modified_cells) == 0:
            return False
        else:
            master_elem = cls.modified_cells.dequeue()
            # On va sortir de modified_cells (Queue) master_elem (Queue), qui
            # contient les positions et les états à modifier

            if isinstance(master_elem, Queue):
                while len(master_elem) != 0:
                    elem = master_elem.dequeue()

                    try:
                        set_type, pos, id = elem
                    except ValueError as e:
                        raise ValueError("Il faut 3 éléments : type de modification, position, type à modifier") from e

                    if set_type == cls.SET_TYPE_WALL:
                        cls.setWall(pos, id, save=False)
                    elif set_type == cls.SET_TYPE_CELL:
                        cls.setCell(pos, id, save=False)
                    else:
                        raise ValueError("Type de modification inconnu")
            else:
                raise ValueError("Pas une Queue")

            return True

    @classmethod
    def __init__(cls) -> None:
        """
        Procédure exécutée lors de l'initialisation de la classe.
        """

        cls.modified_cells = Queue()
        # Cellules à modifier, pour l'affichage

        cls.modified_cells_tmp = Queue()
        # Permet de modifier plusieurs cellules par frame

        width = Settings.get("WIDTH", int)
        ratio = Settings.get("WIDTH_RATIO", str)

        ratio = ratio.split(':')

        height = float(ratio[1])/float(ratio[0]) * width
        height = round(height)

        cls.dimensions = [(x, y) for x in range(width)
                                 for y in range(height)]
        # Initialisation d'une liste comprenant toutes les composantes (x, y),
        # utile pour pouvoir parcourir facilement la map

        cls.map = []
        # Grille à 2 dimensions

        cls.real_width = width*2 + 1
        cls.real_height = height*2 + 1
        # Taille réelle en prenant en compte les murs et les intersections

        cls.width = width
        cls.height = height

        for x in range(cls.real_width):
            # Création de la grille

            line = []

            for y in range(cls.real_height):
                if x%2 == 0 or y%2 == 0:
                    # Génération des intersections

                    id = Map.WALL
                else:
                    # Génération des cellules

                    id = Map.EMPTY

                line.append(id)

            cls.map.append(line)

        cls.start_pos = None
        cls.goal_pos = None

    @classmethod
    def isCellPosValid(cls, pos:Position) -> bool:
        """
        Fonction permettant de savoir si une position de case est valide.
        Exemple de position de cellule valide   : (1  , 4)
        Exemple de position de cellule invalide : (1.5, 4)
        Exemple de position de cellule invalide : (-1 , 4)

        INPUT :
            pos : Position, position (x, y) entière positive

        OUTPUT :
            valid : bool, si la position est valide ou non
        """

        if isinstance(pos, tuple):
            pos = Position(pos)

        valid = True

        if pos.x not in range(cls.width):
            # Si x < 0 ou x >= largeur
            valid = False

        if pos.y not in range(cls.height):
            # Si y < 0 ou y >= hauteur
            valid = False

        return valid

    @classmethod
    def getCell(cls, pos:Position) -> int:
        """
        Fonction retournant la valeur d'une case

        INPUT :
            pos : Position, position (x, y) entière positive

        OUTPUT :
            etat : int, un type de cellule

        EXCEPTION :
            ValueError : si la position de la cellule est invalide
        """

        if isinstance(pos, tuple):
            pos = Position(pos)

        if not cls.isCellPosValid(pos):
            raise ValueError("Position de cellule invalide : pos=" + str(pos))

        pos = cls.truePos(pos)

        etat = cls.map[pos.x][pos.y]

        return etat

    @classmethod
    def setCell(cls, pos:Position, id:int, save:bool=True) -> None:
        """
        Fonction permettant de modifier la valeur d'une case

        INPUT :
            pos : Position, position (x, y) entière positive
            id : int, un type de cellule
            save : bool, s'il faut sauvegarder cette modification pour l'affichage

        EXCEPTION :
            ValueError : si la position est invalide
        """

        if isinstance(pos, tuple):
            pos = Position(pos)

        if not cls.isCellPosValid(pos):
            raise ValueError("Position de cellule invalide")

        if save:
            cls.modified_cells_tmp.enqueue((cls.SET_TYPE_CELL, pos, id))

        pos = cls.truePos(pos)

        cls.map[pos.x][pos.y] = id

    @classmethod
    def syncModifiedCells(cls) -> None:
        """
        Permet de synchroniser les modifications, pour par exemple modifier
        plusieurs cellules par frame
        """

        cls.modified_cells.enqueue(cls.modified_cells_tmp)

        cls.modified_cells_tmp = Queue()

    @classmethod
    def isWallPosValid(cls, pos:Position) -> bool:
        """
        Fonction permettant de savoir si une position de mur est valide.

        INPUT :
            pos : Position, position (x, y) positive ayant pour partie
                            flottante 0.5 en x ou (exclusif) en y
                            Exemple : (0.5, 1) et (4, 5.5) sont valides, mais
                            pas (9.5, 7.5), (7, 4) ou encore (-8, 0)

        OUTPUT :
            valid : bool, si la position est valide ou non
        """

        if isinstance(pos, tuple):
            pos = Position(pos)

        valid = (pos.x % 1 == 0.5) ^ (pos.y % 1 == 0.5)
        # L'opérateur '^' est l'opérateur XOR
        # On veur en effet que x = n+0.5 XOR y = n+0.5 (n entier)
        # Une et une seule des 2 valeurs doit être entière
        # En effet, si les 2 sont entières c'est une case,
        # et si les 2 sont flottantes c'est une intersection (non modifiable)

        pos = cls.truePos(pos)

        if pos.x not in range(1, cls.real_width-1):
            # On exclut les nombres négatifs et les positions hors du jeu
            # On exclut aussi les murs extérieurs, non modifiables
            # On exclut donc x <= 1 et x >= largeur-1
            valid = False

        if pos.y not in range(1, cls.real_height-1):
            valid = False

        return valid

    @classmethod
    def getWall(cls, pos:Position) -> int:
        """
        Fonction retournant la valeur d'un mur.

        INPUT :
            pos : Position, position (x, y) positive ayant pour partie
                            flottante 0.5 en x ou (exclusif) en y
                            Exemple : (0.5, 1) et (4, 5.5) sont valides, mais
                            pas (9.5, 7.5), (7, 4) ou encore (-8, 0)

        OUTPUT :
            etat : int, un type de mur

        EXCEPTION :
            ValueError, si la position du mur n'est pas valide
        """

        if isinstance(pos, tuple):
            pos = Position(pos)

        if not cls.isWallPosValid(pos):
            raise ValueError("Position de mur invalide : pos=" + str(pos))

        pos = cls.truePos(pos)

        etat = cls.map[pos.x][pos.y]

        return etat

    @classmethod
    def setWall(cls, pos:Position, id:int, save:bool=True) -> None:
        """
        Fonction permettant de modifier la valeur d'un mur.

        INPUT :
            pos : Position, position (x, y) positive ayant pour partie
                            flottante 0.5 en x ou (exclusif) en y
                            Exemple : (0.5, 1) et (4, 5.5) sont valides, mais
                            pas (9.5, 7.5), (7, 4) ou encore (-8, 0)
            id : int, un type de mur
            save : bool,  s'il faut sauvegarder cette modification pour l'affichage

        OUTPUT :
            None

        EXCEPTION :
            ValueError, si la position du mur n'est pas valide
        """

        if isinstance(pos, tuple):
            pos = Position(pos)

        if not cls.isWallPosValid(pos):
            raise ValueError("Position de mur invalide")

        if save:
            cls.modified_cells_tmp.enqueue((cls.SET_TYPE_WALL, pos, id))

        pos = cls.truePos(pos)

        cls.map[pos.x][pos.y] = id

    @classmethod
    def truePos(cls, pos:Position) -> Position:
        """
        Fonction permettant d'avoir de vraies coordonnées à partir des
        coordonnées que le reste du programme voit.

        Exemple : la case (2  , 1) a pour position réelle (5, 3)
                          (2.5, 1) a pour position réelle (6, 3)
                          (0  , 0) a pour position réelle (1, 1)

        INPUT :
            pos : objet Position, position (x, y) positive
        """

        pos = Position(pos)

        pos = pos*2 + (1, 1)

        pos.x = round(pos.x)
        pos.y = round(pos.y)

        return pos

    @classmethod
    def displayAsText(cls) -> None:
        """
        Fonction affichant la map dans la console Python.
        """

        print('\n'*30)

        for y in range(cls.real_height):
            for x in range(cls.real_width):
                etat = cls.map[x][y]

                dico = {Map.EMPTY        :' ',
                        Map.WALL         :'█',
                        Map.RED_WALL     :'▓',
                        Map.START        :'«',
                        Map.GOAL         :'»',
                        Map.YELLOW_CELL  :'*',
                        Map.ORANGE_CELL  :'×',
                        Map.VISITED_PATH :'*',
                        Map.SOLUTION_PATH:'$',
                        Map.NOT_VISITED  :'-'}

                try:
                    s = dico[etat]
                except KeyError:
                    s = '?'

                print(s, end='')
                # On affiche chaque caractère sans retour à la ligne

            print() # Retour à la ligne

    @classmethod
    def rangeDimension(cls) -> list:
        """
        Fonction permettant juste de compresser

        for x in range(width):
            for y in range(height):
                ...

        en

        for x, y in rangeDimension():
            ...

        INPUT :
            cls : classe Map, paramètre geré automatiquement par Python

        OUTPUT :
            list tuple, liste de coordonnées (x, y)
        """

        raise NotImplementedError()

        return cls.dimensions

    @classmethod
    def importMap(cls, filename:str) -> None:
        raise NotImplementedError()

    @classmethod
    def exportMap(cls, filename:str) -> None:
        raise NotImplementedError()
