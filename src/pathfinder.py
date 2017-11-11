import os
import sys

# ------ Fonctions ------

# 1. Obtenir le main_path

def main_path():
    """
    Retourne le main_path du projet
    """
    main_path_split = os.getcwd().split(os.sep)
    while main_path_split[-1] != "Rush_Hour":
        main_path_split.pop()
    main_path = ""
    for elt in main_path_split:
        main_path += elt + os.sep
    return main_path[:-len(os.sep)]


# 2. Le pathfinder
def get_path(fullname):
    """
    Fonction qui retourne le chemin d'un fichier ou dossier
    à partir d'un fullname
    fullname est un string du type "image_num.format"
    """
    # 1. Variables
    main = main_path()
    formats = ["png", "txt", "ttf", "wav", "py", "mp3"]
    places = ["images", "music", "src", ""]
    name = fullname.partition(".")[0]
    end = fullname.partition(".")[2]
    labels = name.partition("_")
    num = labels[1]
    path = ""

    # 2. Vérification de la conformité de fullname
    if end not in formats and end != "":
        raise UserWarning("Le format de {0} n'est pas supporté".format(fullname))

    # 3. Recherche
    for place in places:
        p = os.path.join(main, place)
        for root, dirs, files in os.walk(p):
            if fullname in dirs:
                path = os.path.join(root, fullname)
                break
            elif fullname in files:
                path = os.path.join(root, fullname)
                break

    # 4. Sortie
    if path == "":
        raise UserWarning("{0} n'a pas été trouvé.".format(fullname))
    else:
        return path
