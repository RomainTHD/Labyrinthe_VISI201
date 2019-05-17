class Stack:
    def __init__(self, *args):
        """
        Crée une pile

        Les arguments donnés sont dans l'ordre : le premier élément sera le
        premier à sortir

        INPUT :
            *args : arguments donnés
                    Utiliser Stack(*[a, b, c]) pour exécuter Stack(a, b, c)
        """

        self._content = []

        for i in range(len(args)-1, -1, -1):
            self.push(args[i])

    def push(self, value:object) -> None:
        """
        Ajoute un élément à la pile

        INPUT :
            value : n'importe quel type, élément à ajouter

        OUTPUT :
            None
        """

        self._content.append(value)

    def pop(self) -> object:
        """
        Sors le premier élément de la pile

        INPUT :
            self : paramètre géré automatiquement par Python

        OUTPUT :
            value : n'importe quel type, élément sorti

        EXCEPTION :
            ValueError : si la pile est vide
        """

        if len(self._content) == 0:
            raise ValueError("Pile vide")

        value = self._content[-1]

        del self._content[-1]

        return value

    def __str__(self):
        """
        Représentation de l'objet
        """

        s = "<-> "
        s += str(self._content[::-1])
        s += ' |'

        return s

    def __len__(self):
        """
        Taille de l'objet

        OUTPUT :
            int, taille de la pile
        """

        return len(self._content)

    def get(self) -> list:
        return self._content[::-1]

if __name__ == "__main__":
    q = Stack(3, 2, 1)
    assert q.get() == [3, 2, 1]

    q.push(4)
    assert q.get() == [4, 3, 2, 1]

    n = q.pop()
    assert n == 4
    assert q.get() == [3, 2, 1]
