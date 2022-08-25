<h1> Projet VISI201 2019</h1>

<em>Ce programme ne nécessite que tkinter et Python 3</em>

Certain paramètres peuvent être changés dans le fichier settings.cfg
<br>
Pour exécuter le programme, lancez `main.py`

Contenu des dossiers :
    <br>
- environment : modules permettant de concevoir l'interface graphique de base et une grille vide
    <br>
- generation : modules générant le labyrinthe
    <br>
- resolution : modules résolvant le labyrinthe

La génération et la résolution sont faites en amont, l'affichage ne fait que retracer ce qui a déjà été calculé. Attention donc aux boucles infinies dans les algoritmes ! Une génération parallèle dans différents threads a aussi été réalisée (mais n'est pas encore sur GitHub).
