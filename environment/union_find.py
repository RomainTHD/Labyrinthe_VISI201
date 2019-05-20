class UnionFind:
    """
    Union–Find

    Met en relations des objets avec un représentant

    Dans cette implémentation de l'algorithme Union-Find, on utilise la
    compression de chemin dans le find afin d'éviter trop de récursions
    """

    def __init__(self, *init_arr) -> None:
        """
        Création de l'objet Union-Find

        INPUT :
            init_arr : liste des objets
        """

        self._repr = {}

        for item in init_arr:
            self._repr[item] = item

    def find(self, elem:object) -> object:
        """
        Trouve le représentant de elem

        INPUT :
            elem : object, objet auquel il faut trouver le représentant

        OUTPUT :
            object, représentant
        """

        try:
            repr = self._repr[elem]
        except KeyError as e:
            raise KeyError("'{0}' n'appartient pas à Union-Find".format(elem)) from e

        if repr != elem:
            repr = self.find(repr)
            self._repr[elem] = repr

        return repr

    def union(self, elem1:object, elem2:object) -> None:
        """
        Réunit les 2 listes, celle contenant elem1 et celle contenant elem2

        INPUT :
            elem1 : object, élément à unir
            elem2 : object, élément à unir
        """

        try:
            repr_elem1 = self.find(elem1)
            repr_elem2 = self.find(elem2)

            self._repr[repr_elem1] = repr_elem2
        except KeyError as e:
            raise KeyError("'{0}' ou '{1}' n'appartient pas à Union-Find".format(elem1, elem2)) from e

    def __str__(self) -> str:
        s = ""

        for repr, item in self._repr.items():
            s += "{0}:{1} - ".format(item, repr)

        return s[:-2]

if __name__ == "__main__":
    t = [i for i in range(10)]

    u = UnionFind(*t)

    u.union(1, 2)

    assert u.find(1) == 2

    u.union(3, 1)

    assert u.find(1) == u.find(2) == u.find(3) != u.find(4)
    assert u.find(0) == 0
