import random

class Position:
    """
    Classe servant à mieux gérer les positions.
    On réunit les composantes x et y en un seul objet.

    NOTE : dans l'aide des fonctions, il est marqué 'Position' au lieu de
           Position car Python ne comprend pas l'utilisation de la classe
           Position à l'intérieur d'elle-même.
    """

    def __init__(self, value:(tuple, 'Position')) -> None:
        """
        Initialisation de l'instance.

        INPUT :
            self : instance de Position
            value : tuple (x, y) ou Position, valeur à affecter

        OUTPUT :
            None
        """

        if isinstance(value, tuple):
            self.x, self.y = value
        elif isinstance(value, Position):
            self.x, self.y = value.x, value.y
        else:
            raise ValueError("Type inconnu. Type : "+str(type(other)))

    @staticmethod
    def random(p_min:('Position', tuple), p_max:('Position', tuple)) -> 'Position':
        """
        Fonction permettant de créer une position aléatoire
        entre (x_min, y_min) et (x_max, y_max)

        INPUT :
            p_min : objet Position, x et y minimal
                    si tuple, couple (x, y)
            p_max : objet Position, x et y maximal
                    si tuple, couple (x, y)

        OUTPUT :
            Position, position aléatoire
        """

        p_min = Position(p_min)
        p_max = Position(p_max)

        x = random.randint(p_min.x, p_max.x)
        y = random.randint(p_min.y, p_max.y)

        return Position((x, y))

    def _basicOperation(self, other:('Position', tuple, int, float), name:str, operation:'function', input_type:tuple) -> 'Position':
        """
        Fonction exécutée lors d'une opération mathématique ou logique avec une
        position, par exeple 'p1 + p2' ou 'p1 == p2'.

        Note : dans les commentaires, 'o' représente l'opération.

        INPUT :
            self : objet Position
            other : Position ou tuple ou int ou float, autre membre de l'opération
            name : str, nom de l'opération
            opération : func, fonction à exécuter sur les membres
            input_type : tuple, type des entrées possibles

        OUTPUT :
            p : Position, nouvelle position
        """

        if Position in input_type and isinstance(other, Position):
            # On récupère le type de la variable 'other'
            # pour savoir s'il s'agit d'un nombre, d'une position, etc...

            # Si Position o Position
            coords = (operation(self.x, other.x), operation(self.y, other.y))
        elif Position in input_type and isinstance(other, tuple):
            # Si Position o (x, y)

            coords = (operation(self.x, other[0]), operation(self.y, other[1]))
        elif int in input_type and isinstance(other, int):
            # Si Position o k avec k entier

            coords = (operation(self.x, other), operation(self.y, other))
        elif float in input_type and isinstance(other, float):
            # Si Position o k avec k flottant

            coords = (operation(self.x, other), operation(self.y, other))
        else:
            # Si c'est une opération par un autre type

            raise ValueError(name + " inconnue, mauvais type. Type : "+str(type(other)))

        p = Position(coords)
        # On crée une nouvelle position

        return p

    def __str__(self) -> str:
        """
        Chaine de caractère utilisée lors d'un print(pos) ou d'un str(pos).

        INPUT :
            self : instance de Position

        OUTPUT :
            s : str, description de l'objet
        """

        s = "Position object at (x:{0}, y:{1})".format(self.x, self.y)

        return 'P:' + self.strPos()

    def __repr__(self) -> tuple:
        return self.__str__()

    def __mul__(self, other:(int, float, tuple, 'Position')) -> 'Position':
        """
        Fonction exécutée par python lorsque l'objet est multiplié.
        Cf Position._basicOperation(self, other, name, operation)

        Utilisé pour p*2 ou p*-1 .

        INPUT :
            self : instance de Position
            other : int ou float ou tuple ou Position, ce qui va être multiplié

        OUTPUT :
            p : Position, nouvelle position
        """

        return self._basicOperation(other, "Multiplication", lambda a, b : a*b, (int, float))

    def __add__(self, other:(int, float, tuple, 'Position')) -> 'Position':
        """
        Fonction exécutée par python lorsque l'objet est additionné.

        Utilisé pour p1+p2 .

        Cf Position.__mul__(self, other)
        """

        return self._basicOperation(other, "Addition", lambda a, b : a+b, (Position, ))

    def __truediv__(self, other:(int, float, tuple, 'Position')) -> 'Position':
        """
        Fonction exécutée par python lorsque l'objet est divisé ('/').

        Utilisé pour p/2 pour avoir des flottants pour les murs.

        Cf Position.__mul__(self, other)
        """

        return self._basicOperation(other, "Division", lambda a, b : a/b, (int, ))

    def __eq__(self, other:('Position', tuple)) -> bool:
        """
        Fonction exécutée par python lors d'un test d'égalité ('==').

        Cf Position.__mul__(self, other)
        """

        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        else:
            raise ValueError("Égalité inconnue, mauvais type. Type : "+str(type(other)))

    def __ne__(self, other:'Position') -> bool:
        """
        Fonction exécutée par python lors d'un test de différence ('!=').

        Cf Position.__mul__(self, other)
        """

        return not self.__eq__(other)

    def __hash__(self) -> hash:
        """
        Méthode utilisée par Python pour les dictionnaires et les sets.
        On veut obtenir le hash de notre Position.
        Pour celà, on utilise le hash du tuple équivalent, qui est déjà
        implémenté par Python.
        """

        return self.toTuple().__hash__()

    def strPos(self, format_nb:int=0) -> str:
        """
        Fonction retournant les coordonnées de l'objet sous forme "(x,y)"

        INPUT :
            format_nb : int, nombre de chiffres à afficher
        """

        s = "({0:0"+str(format_nb)+"},{1:0"+str(format_nb)+"})"
        s = s.format(self.x, self.y)

        return s

    def toTuple(self) -> tuple:
        return (self.x, self.y)
