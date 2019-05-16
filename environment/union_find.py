class UnionFind:
    """
    Union–Find, alias Disjoint-Set

    Met en relations des objets avec un représentant
    """

    def __init__(self, *init_arr) -> None:
        """
        Création de l'objet Union-Find.

        INPUT :
            init_arr : liste des objets
        """

        self._repr = {}

        for item in init_arr:
            self._repr[item] = item

    def _find_repr(self, elem:object) -> object:
        """
        Trouve le représentant d'un objet.

        INPUT :
            elem : object, objet auquel il faut trouver le représentant

        OUTPUT :
            repr : object, représentant

        EXCEPTION :
            KeyError, si l'élément n'est pas dans l'objet Union-Find
        """

        try:
            repr = self._reversed_dict[elem]
        except KeyError as e:
            raise KeyError("L'élément '{0}' n'appartient pas à l'instance Union-Find".format(elem)) from e
        else:
            return repr

    def find(self, elem:object, n=0) -> list:
        """
        Trouve la liste contenant elem

        INPUT :
            elem : object, objet auquel il faut trouver la liste dans laquelle
                           il est contenu

        OUTPUT :
            list, liste des éléments, contient forcément elem
        """

        repr = self._repr[elem]

        if repr != elem:
            repr = self.find(repr, n+1)
            self._repr[elem] = repr

        return repr

    def union(self, elem1:object, elem2:object) -> list:
        """
        Réunit les 2 listes, celle contenant elem1 et celle contenant elem2.
        """

        try:
            repr_elem1 = self.find(elem1)
            repr_elem2 = self.find(elem2)

            self._repr[repr_elem1] = repr_elem2
        except KeyError as e:
            raise KeyError("'{0}' ou '{1}' n'appartient pas à Union-Find".format(elem1, elem2)) from e

    def __str__(self) -> str:
        """
        s = ""

        for repr, item in self._repr.items():
            s += "{0}:{1} - ".format(item, repr)

        return s[:-2]
        """

        s1 = ""
        s2 = ""

        max_size = 0

        for repr, item in self._repr.items():
            if len(str(repr)) > max_size:
                max_size = len(str(repr))

            if len(str(item)) > max_size:
                max_size = len(str(item))

        for repr, item in self._repr.items():
            repr_str = str(repr)
            item_str = str(item)

            while len(repr_str) < max_size:
                repr_str = ' ' + repr_str

            while len(item_str) < max_size:
                item_str = ' ' + item_str

            s1 += repr_str + ' - '
            s2 += item_str + ' - '

        return s1[:-3] + '\n' + s2[:-3]

if __name__ == "__main__d":
    t = [i for i in range(10)]

    u = UnionFind(*t)

    u.union(1, 2)

    assert u.find(1) == 2

    u.union(3, 1)

    print(u.find(1))
    print(u.find(2))
    print(u.find(3))
    print(u.find(4))

    assert u.find(1) == u.find(2) == u.find(3) != u.find(4)
    assert u.find(0) == 0

if __name__ == "__main__":
    t = [i for i in range(50)]

    u = UnionFind(*t)

    from random import randrange

    for i in range(20):
        a = randrange(50)
        b = randrange(50)

        u.union(a, b)

    print(u)
