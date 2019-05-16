class Settings:
    @classmethod
    def __init__(cls) -> None:
        """
        Fonction pour charger les paramètres.

        Les paramètres sont en majuscule, et les espaces sont retirés.
        Exemple : "val = 0" devient "VAL=0"

        Des commentaires sont possibles avec '#'
        Exemple : "val = 0 # Valeur de quelque chose" devient "VAL=0",
        le commentaire n'est pas lu.

        INPUT :
            cls : classe Settings, paramètre géré automatiquement par Python.

        OUTPUT :
            None

        EXCEPTION :
            FileNotFoundError : si le fichier n'existe pas
        """

        try:
            settings_file = open("settings.cfg", 'r')
        except FileNotFoundError:
            raise FileNotFoundError("Pas de fichier configuration settings.cfg !")

        cls.settings = {}

        line = settings_file.readline()

        while line != '':
            line = line.upper().replace(' ', '').replace('\n', '')
            # On retire les espaces et les retours à la ligne

            if len(line) != 0:
                # Pour éviter les commentaires et les lignes vides

                line = line.split('#')[0]
                # Si une ligne est sous forme "PARAM = VALUE # COMMENTAIRE",
                # on ne garde que "PARAM = VALUE"

                line = line.split('=')

                if len(line) == 2:
                    cls.settings[line[0]] = line[1]

            line = settings_file.readline()

        settings_file.close()

        #! print("SETTINGS :", cls.settings)

    @classmethod
    def get(cls, key:str, return_type:type) -> (str, int, float, bool):
        """
        Fonction pour récupérer un paramètre.

        INPUT :
            cls : classe Settings, paramètre géré automatiquement par Python.
            key : str, nom du paramètre.
            return_type : type, type du paramètre (str, int, bool...)

        OUTPUT :
            val : str ou int ou float ou bool, valeur du paramètre

        EXCEPTION :
            ValueError : s'il n'y a pas de paramètre, ou si le type est incohérent
        """

        key = key.upper()

        try:
            val = cls.settings[key]
        except KeyError:
            raise ValueError("Ligne absente")

        if return_type is str:
            pass
        elif return_type is int:
            try:
                val = int(val)
            except ValueError:
                raise ValueError("Pas un entier")
        elif return_type is float:
            try:
                val = float(val)
            except ValueError:
                raise ValueError("Pas un float")
        elif return_type is bool:
            if val in ("Y", "YES", "T", "TRUE", "1"):
                val = True
            elif val in ("N", "NO", "F", "FALSE", "0"):
                val = False
            else:
                raise ValueError("Pas un booléen")
        else:
            raise ValueError("Type incorrect")

        return val
