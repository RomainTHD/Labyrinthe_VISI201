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

        self._disjoint_set = {}
        self._reversed_dict = {}

        if init_arr is not None:
            for item in init_arr:
                self._disjoint_set[item] = [item]
                self._reversed_dict[item] = item

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

    def find(self, elem:object) -> list:
        """
        Trouve la liste contenant elem

        INPUT :
            elem : object, objet auquel il faut trouver la liste dans laquelle
                           il est contenu

        OUTPUT :
            list, liste des éléments, contient forcément elem
        """

        key = self._find_repr(elem)

        return self._disjoint_set[key]

    def union(self, elem1:object, elem2:object) -> list:
        """
        Réunit les 2 listes, celle contenant elem1 et celle contenant elem2.
        """

        repr_elem1 = self._find_repr(elem1)
        repr_elem2 = self._find_repr(elem2)

        if repr_elem1 != repr_elem2:
            if len(self._disjoint_set[repr_elem1]) > len(self._disjoint_set[repr_elem2]):
                self._disjoint_set[repr_elem1].extend(self._disjoint_set[repr_elem2])

                for elem in self._disjoint_set[repr_elem2]:
                    self._reversed_dict[elem] = repr_elem1

                del self._disjoint_set[repr_elem2]
            else:
                self._disjoint_set[repr_elem2].extend(self._disjoint_set[repr_elem1])

                for elem in self._disjoint_set[repr_elem1]:
                    self._reversed_dict[elem] = repr_elem2

                del self._disjoint_set[repr_elem1]

    def get(self) -> dict:
        """
        Retourne le dictionnaire associé.
        """

        return self._disjoint_set

    def __str__(self) -> str:
        dico = self.get()

        s = ""

        for k in dico.keys():
            s += "{0}:{1} - ".format(k, dico[k])

        return s[:-2]

if __name__ == "__main__":
    t = [i for i in range(10)]

    u = UnionFind(*t)

    print(u)
    #   "0:[0] - 1:[1] - 2:[2] - 3:[3] - 4:[4] - 5:[5] - 6:[6] - 7:[7] - 8:[8] - 9:[9]"

    u.union(1, 5)
    u.union(1, 3)

    print(u)
    #    "0:[0] - 2:[2] - 4:[4] - 5:[5, 1, 3] - 6:[6] - 7:[7] - 8:[8] - 9:[9]"

    print(u.find(1))
    #   "[5, 1, 3]"
