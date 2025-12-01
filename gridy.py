import pandas


class Cellule:
    def __init__(self, texte):
        self.texte = texte      # texte brut de la cellule (ex: "3", "=A1+2")
        self.valeur = None      # valeur numérique ou texte après calcul
        self.en_cours = False   # pour détecter les cycles


def indice_to_colonne(ind):
    # convertit un indice de colonne (0,1,2,...) en 'A','B',..., 'AA', etc.
    resultat = ""
    while True:
        ind, reste = divmod(ind, 26)
        lettre = chr(ord('A') + reste)
        resultat = lettre + resultat
        if ind == 0:
            break
        ind -= 1
    return resultat


def creer_dico(fichier):
    nb_lignes, nb_colonnes = fichier.shape
    grille = {}

    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            lettre_colonne = indice_to_colonne(j)
            numero_ligne = i + 1
            nom_cellule = f"{lettre_colonne}{numero_ligne}"

            texte = fichier.iat[i, j]
            if pandas.isna(texte):
                texte = ""

            cellule = Cellule(str(texte))

            # initialiser la valeur directement si ce n'est pas une formule
            if not cellule.texte.startswith("="):
                txt = cellule.texte
                if txt == "":
                    cellule.valeur = ""
                else:
                    try: # on essaye de convertir en nombre, si erreur alors c'est du texte
                        cellule.valeur = float(txt)
                    except ValueError:
                        cellule.valeur = txt 
            grille[nom_cellule] = cellule # on ajoute la cellule au dictionnaire

    return grille


# fonctions pour les formules
def SUM(*args):
    return sum(args)


def AVG(*args):
    return sum(args) / len(args) if args else 0

def COUNT(*args):
    return len(args)

#def COUNTA(*args):


# fonction principale pour évaluer une cellule

def evaluer_cellule(nom, dico, valeurs):
    cellule = dico[nom]

    # pour détecter les cycles
    if cellule.en_cours:
        cellule.valeur = "#CYCLE"
        valeurs[nom] = cellule.valeur
        return cellule.valeur

    # si on connait déja la valeur, on ne va pas la recalculer
    if cellule.valeur is not None:
        return cellule.valeur


    if not cellule.texte.startswith("="):     # si c'est pas une formule, c'est soit une chaîne vide, soit une valeur numérique, soit du texte
        texte = cellule.texte
        if texte == "":
            cellule.valeur = ""
        else: # si ce n'est pas une chaine vide, on vérifie si c'est un nombre
            try:
                cellule.valeur = float(texte)
            except ValueError:
                cellule.valeur = texte
        # si ce n'est pas un nombre ou une formule, c'est du texte
        valeurs[nom] = cellule.valeur
        return cellule.valeur

    # c'est une formule, on évalue (sauf si il y a une erreur dans la formule, dans ce cas on affiche #ERREUR)
    cellule.en_cours = True
    formule = cellule.texte[1:]

    # on évalue la formule en utilisant le dictionnaire des valeurs
    try:
        cellule.valeur = eval(formule, valeurs)
    except Exception:
        cellule.valeur = "#ERREUR"

    cellule.en_cours = False
    valeurs[nom] = cellule.valeur # on remplit le dictionnaire des valeurs avec la valeur calculée
    return cellule.valeur





# fonction pour afficher le dictionnaire de cellules

def afficher_dico(dico):
    affichage = []

    for nom in dico.keys():
        cellule = dico[nom]
        valeur_str = str(cellule.valeur) if cellule.valeur is not None else "None"
        affichage.append(f"'{nom}' : ('{cellule.texte}', {valeur_str})")

    print("----------------------------")
    print(",\n".join(affichage)) 
    print("----------------------------")


"""Programme principal"""


fichier = pandas.read_csv("test.csv", header=None)
dico = creer_dico(fichier)

# on initialise le dictionnaire des valeurs avec les fonctions, qui passera en paramètre à eval

valeurs = {
    "SUM": SUM,
    "AVG": AVG,
    "MAX": max,
    "MIN": min,
}

for nom, cellule in dico.items():
    if cellule.valeur is not None:
        valeurs[nom] = cellule.valeur

# on rajoute les valeurs déja connues dans le dictionnaire des valeurs
for nom in dico:
    evaluer_cellule(nom, dico, valeurs)


afficher_dico(dico)
