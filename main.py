import sys

if sys.version_info <= (3, 0):
    sys.stdout.write("Python 2 détecté, fermeture du programme\n")
    sys.exit(1)

from environment.display import Display
# Gestion de l'affichage fenêtre

from environment.map import Map
# Plateau de jeu

from environment.settings import Settings
Settings.__init__()
# Chargement des paramètres du fichier settings.cfg

################################################################################
# Dans cette partie, on va paramétrer l'aléatoire avec une graine.
# Une même graine donnera toujours le même résultat.

import random

seed = Settings.get("SEED", int)

if seed == -1:
    seed = random.randrange(0, 10**9)

print("Graine aléatoire : {0:09}".format(seed))

random.seed(seed)

################################################################################
# Importation de l'algorithme de génération

algo_name = Settings.get("ALGO_GEN", str)

if algo_name == "RECURSIVE_BACKTRACKER_GEN":
    from generation.recursive_backtracker_gen import Generation
elif algo_name == "KRUSKAL":
    from generation.kruskal import Generation
else:
    raise ValueError("Algorithme non reconnu : " + algo_name)

################################################################################
# Importation de l'algorithme de résolution

algo_name = Settings.get("ALGO_RES", str)
allow_resolution = True

if algo_name == "NONE":
    allow_resolution = False
elif algo_name == "RIGHT_HAND":
    from resolution.right_hand import Resolution
elif algo_name == "RECURSIVE_BACKTRACKER_RES":
    from resolution.recursive_backtracker_res import Resolution
else:
    raise ValueError("Algorithme non reconnu : " + algo_name)

################################################################################

gen = Generation()

if allow_resolution:
    res = Resolution()
    res_name = res.ALGORITHM_NAME
else:
    res_name = "None"

Map.__init__()
Display.__init__(gen_name=gen.ALGORITHM_NAME, res_name=res_name)
# Initialisation du terrain et de la fenêtre

gen.start()
# Lancement de la génération

if allow_resolution:
    res.start()
    # Lancement de la résolution

Map.resetAll(save=False)
# On réinitialise la grille

Display.run()
# Lancement de l'affichage

"""
985085517
"""
