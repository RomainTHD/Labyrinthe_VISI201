class Queue:
    def __init__(self, *args):
        """
        Crée une file

        Les arguments donnés sont dans l'ordre : le premier élément sera le
        dernier à sortir

        INPUT :
            *args : arguments donnés
                    Utiliser Queue(*[a, b, c]) pour exécuter Queue(a, b, c)
        """

        self._content = []

        for i in range(len(args)-1, -1, -1):
            self.enqueue(args[i])

    def enqueue(self, value:object) -> None:
        """
        Ajoute un élément à la file

        INPUT :
            value : n'importe quel type, élément à ajouter

        OUTPUT :
            None
        """

        self._content.append(value)

    def dequeue(self) -> object:
        """
        Sors le premier élément de la pile

        INPUT :
            None

        OUTPUT :
            value : n'importe quel type, élément sorti

        EXCEPTION :
            ValueError : si la file est vide
        """

        if len(self._content) == 0:
            raise ValueError("File vide")

        value = self._content[0]

        del self._content[0]

        return value

    def __str__(self) -> str:
        """
        Représentation de l'objet
        """

        s = "> "
        s += str(self._content[::-1])
        s += ' >'

        return s

    def __len__(self) -> int:
        """
        Taille de l'objet, utilisé par la fonction len

        OUTPUT :
            int, taille de la file
        """

        return len(self._content)

if __name__ == "__main__":
    q = Queue(1, 2, 3)
    print(q)
    #   "> [3, 2, 1] >"

    q.enqueue(4)
    print(q)
    #    "> [4, 3, 2, 1] >"

    n = q.dequeue()
    print(n)
    #   "1"
    print(q)
    #   "> [4, 3, 2] >"
