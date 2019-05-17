import tkinter as Tk
# Gestion des fenêtres

try:
    from environment.map import Map
    from environment.direction import Direction
    from environment.settings import Settings
    from environment.position import Position
except ImportError:
    from map import Map
    from direction import Direction
    from settings import Settings
    from position import Position

import time

class Display:
    """
    Classe s'occupant de l'affichage de la fenêtre.
    """

    @classmethod
    def __init__(cls, gen_name:str, res_name:str) -> None:
        """
        Procédure exécutée lors de l'initialisation de la classe.

        INPUT :
            gen_name : str, nom de l'algorithme de génération utilisé
            res_name : str, nom de l'algorithme de résolution utilisé
        """

        ########################################################################
        # Définition des couleurs

        cls.LIGHT_RED  = cls.hsv_to_hex(  0,  33, 100)
        cls.RED        = cls.hsv_to_hex(  0,  100, 67)
        cls.ORANGE     = cls.hsv_to_hex( 30,  80, 100)
        cls.YELLOW     = cls.hsv_to_hex( 60,  67, 100)
        cls.GREEN      = cls.hsv_to_hex(120, 100, 67)
        cls.BLUE       = cls.hsv_to_hex(240, 100, 100)
        cls.LIGHT_BLUE = cls.hsv_to_hex(240,  33, 100)
        cls.BLACK      = "#000000"
        cls.GRAY       = cls.hsv_to_hex(  0,   0,  50)
        cls.LIGHT_GRAY = cls.hsv_to_hex(  0,   0,  75)
        cls.WHITE      = "#ffffff"

        cls.color_scheme = {Map.EMPTY         : cls.WHITE,
                            Map.WALL          : cls.BLACK,
                            Map.RED_WALL      : cls.RED,
                            Map.START         : cls.RED,
                            Map.GOAL          : cls.GREEN,
                            Map.YELLOW_CELL   : cls.YELLOW,
                            Map.ORANGE_CELL   : cls.ORANGE,
                            Map.SOLUTION_PATH : cls.LIGHT_BLUE,
                            Map.VISITED_PATH  : cls.LIGHT_RED,
                            Map.NOT_VISITED   : cls.LIGHT_GRAY,}
        # On associe chaque type de case à une couleur

        ########################################################################
        # Création de la fenêtre

        cls.window = Tk.Tk() # Fenêtre d'origine
        cls.gen_name = gen_name
        cls.res_name = res_name

        cls.window.resizable(width=True, height=True)

        ########################################################################
        # Quelques variables utiles

        frame_rate = Settings.get("FRAME_RATE", float)
        # On récupère le nombre d'images par seconde

        cls.is_running = True
        # Variable pour savoir si la fenêtre est fermée ou non

        cls.frame_count = 0
        # Nombre d'images écoulées

        cls.time_between_frame = 1/frame_rate
        # Temps entre 2 images

        cls.draw_time = cls.time_between_frame

        cls.time_before_draw = time.time()

        cls.skipped_frame = 0

        window_zoom = Settings.get("WINDOW_ZOOM", float)

        window_width = cls.window.winfo_screenwidth()*window_zoom/100
        # On récupère la largeur que doit avoir la fenêtre

        width = Settings.get("WIDTH", int)
        # On récupère le nombre de cellules en largeur

        cell_size = window_width/width
        # On calcule la taille d'une cellule

        cls.cell_size = int(cell_size)

        cls.width = int(Map.width * cls.cell_size)
        cls.height = int(Map.height * cls.cell_size)
        # Largeur et hauteur de la fenêtre

        cls.grille = Tk.Canvas(cls.window,
                               width=cls.width,
                               height=cls.height,
                               bg=Display.WHITE)

        cls.grille.grid(row=0, column=0)
        # Création du Canvas sur lequel dessiner les cases

        cls.WALL_WIDTH = 2

        ########################################################################
        # Gestion de la fenêtre au niveau des périphériques

        cls.window.protocol("WM_DELETE_WINDOW", cls.quit)
        cls.window.bind("<Escape>", cls.quit)
        # Gestion des différents événements
        # (croix rouge pour fermer la fenêtre, touche Échap)

        ws = cls.window.winfo_screenwidth()
        hs = cls.window.winfo_screenheight()
        w = cls.width + 3
        h = cls.height + 3
        # On récupère la largeur et la hauteur de l'écran et de la fenêtre
        # Le '+ 3' permet de voir les murs extérieurs de la map

        x = (ws-w)//2
        y = (hs-h)//2

        cls.window.geometry("{0}x{1}+{2}+{3}".format(w, h, x, y))
        # On centre la fenêtre au milieu de l'écran

    @classmethod
    def beforeDraw(cls) -> None:
        """
        Méthode qui s'exécute avant l'affichage de la fenêtre
        """

        if cls.is_running:
            while time.time()-cls.time_before_draw < cls.time_between_frame:
                time.sleep(0.01)

            can_display = Map.modifyCell()

            for i in range(int(cls.draw_time/cls.time_between_frame)):
                Map.modifyCell()
                cls.skipped_frame += 1

            if can_display:
                cls.time_before_draw = time.time()

                cls.draw()
            else:
                print("Affichage final")

    @classmethod
    def draw(cls) -> None:
        """
        Procédure pour dessiner à l'écran.
        """

        t1 = time.time()
        # Repère temporel pour savoir la durée d'un affichage

        if not cls.is_running:
            # Si la fenêtre est fermée on arrête
            return

        cls.grille.delete(Tk.ALL)
        # On réinitialise la grille

        ########################################################################
        # On dessine les cellules

        # On va parcourir la map ligne par ligne
        # pour chercher les cellules adjacentes de même couleur
        # pour ne dessiner qu'un seul rectange plutot que plusieurs carrés.
        # tkinter supporte mal plusieurs centaines de formes à afficher

        for y in range(Map.height):
            first_p = Position((0, y))
            old_p = Position(first_p)

            for x in range(Map.width):
                new_p = Position((x, y))

                if Map.getCell(first_p) == Map.getCell(new_p):
                    pass
                else:
                    cls.drawCell(first_p, old_p)
                    first_p = Position(new_p)

                old_p = Position(new_p)

            cls.drawCell(first_p, old_p)

        ########################################################################
        # On dessine les murs

        # Murs verticaux
        for x in range(Map.width-1):
            first_p = Position((x+0.5, 0))
            old_p = Position(first_p)

            for y in range(Map.height):
                new_p = Position((x+0.5, y))

                if Map.getWall(first_p) == Map.getWall(new_p):
                    pass
                else:
                    cls.drawWall(first_p, old_p, vertical=True)

                    first_p = Position(new_p)

                old_p = Position(new_p)

            cls.drawWall(first_p, old_p, vertical=True)

        # Murs horizontaux
        for y in range(Map.height-1):
            first_p = Position((0, y+0.5))
            old_p = Position(first_p)

            for x in range(Map.width):
                new_p = Position((x, y+0.5))

                if Map.getWall(first_p) == Map.getWall(new_p):
                    pass
                else:
                    cls.drawWall(first_p, old_p, horizontal=True)

                    first_p = Position(new_p)

                old_p = Position(new_p)

            cls.drawWall(first_p, old_p, horizontal=True)

        ########################################################################
        # On dessine les 4 murs extérieurs

        # Mur vertical gauche
        cls.grille.create_line(3,
                               0,
                               3,
                               Map.height*cls.cell_size,
                               fill=Display.BLACK,
                               width=cls.WALL_WIDTH)

        # Mur vertical droit
        cls.grille.create_line(cls.width,
                               0,
                               cls.width,
                               Map.height*cls.cell_size,
                               fill=Display.BLACK,
                               width=cls.WALL_WIDTH)

        # Mur horizontal en haut
        cls.grille.create_line(0,
                               3,
                               Map.width*cls.cell_size,
                               3,
                               fill=Display.BLACK,
                               width=cls.WALL_WIDTH)

        # Mur horizontal en bas
        cls.grille.create_line(0,
                               Map.height*cls.cell_size,
                               Map.width*cls.cell_size,
                               Map.height*cls.cell_size,
                               fill=Display.BLACK,
                               width=cls.WALL_WIDTH)

        cls.frame_count += 1

        cls.updateTitle()

        delta_t = time.time() - t1
        # Calcul du temps mis

        cls.draw_time = delta_t

        cls.window.after(1, cls.beforeDraw)
        # Après un certain temps, on revient à beforeDraw

    @classmethod
    def drawWall(cls, p1:Position, p2:Position, vertical:bool=False, horizontal:bool=False) -> None:
        """
        Affiche une ligne de plusieurs murs

        INPUT :
            p1 : Position, position de la première cellule
            p2 : Position, position de la dernière cellule
            vertical : bool, si c'est un mur vertical
            horizontal : bool, si c'est un mur horizontal

        EXCEPTIONS :
            ValueError : si l'état du mur est inconnu, ou si aucune couleur
                         n'est associée à l'état
        """

        if vertical:
            p1_screen = (p1+(0.5,0))*cls.cell_size
            p2_screen = (p2+(0.5,1))*cls.cell_size
            etat = Map.getWall(p1)
        else:
            p1_screen = (p1+(0,0.5))*cls.cell_size
            p2_screen = (p2+(1,0.5))*cls.cell_size
            etat = Map.getWall(p1)

        if etat != Map.EMPTY:
            width = cls.WALL_WIDTH

            if etat == Map.RED_WALL:
                # Si c'est un mur rouge, on le met en gras

                width = 5

            try:
                color = cls.color_scheme[etat]
            except KeyError as e:
                raise ValueError("État de mur inconnu : " + str(etat)) from e

            # On dessine une ligne allant de p1 à p2
            cls.grille.create_line(p1_screen.x, p1_screen.y, p2_screen.x, p2_screen.y,
                                   fill=color, width=width)

    @classmethod
    def drawCell(cls, p1:Position, p2:Position) -> None:
        """
        Affiche une ligne de plusieurs cellules de même couleur

        INPUT :
            p1 : Position, position de la première cellule
            p2 : Position, position de la dernière cellule

        EXCEPTIONS :
            ValueError : si l'état de la cellule est inconnu
            ValueError : si une cellule est en fait un mur
        """

        etat = Map.getCell(p1)

        if etat != Map.EMPTY:
            try:
                color_in = cls.color_scheme[etat]
            except KeyError as e:
                raise ValueError("Couleur inconnue : "+str(etat)) from e

            if etat == Map.WALL:
                raise ValueError("Il y a un mur sur une case (!)")

            color_out = color_in

            p1 = p1*cls.cell_size
            p2 = p2 + (1, 1)
            p2 = p2*cls.cell_size

            # On dessine un rectange allant de p1 à p2
            cls.grille.create_rectangle(p1.x+1, p1.y+1, p2.x, p2.y,
                                        outline=color_out, fill=color_in)

    @classmethod
    def run(cls) -> None:
        """
        Procédure pour faire tourner la fenêtre.
        """

        cls.beforeDraw()

        cls.window.mainloop()

    @classmethod
    def quit(cls, event=None) -> None:
        """
        Procédure exécutée lorsque l'utilisateur ferme la fenêtre.

        INPUT :
            event : événement tkinter, paramètre inutile ici mais tkinter donne
                    forcément ce paramètre à la fonction, on le prend donc en
                    compte. Autre solution possible : utiliser *args
        """

        cls.is_running = False

        cls.window.destroy()
        # On détruit la fenêtre

        print("Affchage arrêté")

    @classmethod
    def updateTitle(cls) -> None:
        """
        Procédure permettant d'actualiser le titre de la fenêtre, pour par
        exemple afficher le nombre d'images passées
        """

        sep = ' '*4 + '-' + ' '*4
        # Séparateur d'informations

        title = "Génération : " + cls.gen_name + sep \
              + "Résolution : " + cls.res_name + sep \
              + "images écoulées : " + str(cls.frame_count) + sep \
              + "images skippées : " + str(cls.skipped_frame) + sep \
              + "vrai framerate : " + (str(int(1/cls.time_between_frame)) if cls.draw_time == 0 else str(int(100/cls.draw_time)/100)) + " fps"

        cls.window.title(title)

    @staticmethod
    def hsv_to_hex(h:int, s:int, v:int) -> str:
        """
        Retourne le code hexadécimal d'une couleur dans l'espace HSV

        INPUT :
            h : int, couleur entre 0 et 360 sur la roue des couleurs
                     0 : rouge, 120 : vert, 260 : bleu, 360 : rouge encore
            s : int, saturation entre 0 et 100, niveau de gris
            v : int, valeur entre 0 et 100, clair ou foncé

        OUTPUT :
            s : str, couleur en hexadécimal. Exemple : '#baaaad'
        """

        # Conversion vers RGB

        h /= 360
        s /= 100
        v /= 100

        if s == 0:
            r = g = b = int(v*255)
        else:
            i = int(h*6)
            f = (h*6)-i
            p = int(255*v*(1-s))
            q = int(255*v*(1-s*f))
            t = int(255*v*(1-s*(1-f)))

            v = int(v*255)

            i %= 6

            if i == 0:
                r, g, b = (v, t, p)
            elif i == 1:
                r, g, b = (q, v, p)
            elif i == 2:
                r, g, b = (p, v, t)
            elif i == 3:
                r, g, b = (p, q, v)
            elif i == 4:
                r, g, b = (t, p, v)
            elif i == 5:
                r, g, b = (v, p, q)

        ########################################################################
        # Conversion vers hexadécimal

        r = hex(int(r))[2:]
        g = hex(int(g))[2:]
        b = hex(int(b))[2:]

        s = "#" + r.rjust(2, '0') + g.rjust(2, '0') + b.rjust(2, '0')

        return s
